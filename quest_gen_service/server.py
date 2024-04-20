from openai import OpenAI
import os
import logging
import requests
from pythonjsonlogger import jsonlogger

import grpc
from generated_code.feedback_service import feedback_service_pb2
from generated_code.feedback_service import feedback_service_pb2_grpc
from concurrent import futures
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt="%(levelname)s %(asctime)s %(module)s %(filename)s %(lineno)s %(message)s"
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

logging.basicConfig(level=logging.INFO)
client = OpenAI(api_key=os.environ["API"])

feedback_type = {
    "part_1" : {"grammar": "4d21f756a96f4a9ea0686ed3c3148f58",
                "structure": "472d9ccec57c4fe18130948fe3d9680e",
                "vocab": "6996aa52be534966a22ad3fc36131a3c"},
    "part_3" : {"grammar": "3b73852365ab451d9aa62481900ea72a",
                "structure": "1ce3517b68464e849c8e8a37a204fea7",
                "vocab": "92ce2a5bbd4c40a0b1ab9a5ac4faecb9"},
    "part_2" : {"grammar": "1153f6eafbba4992b1029c2ed665e0d4",
                "structure": "f67473da0d7c446dbb21117d1de02881",
                "vocab": "e65d14f4ea8147ce80814a7d83736518"}
}

feedback_type_local = {
    "part_1" : {"grammar": "./prompts/part1_grammar.txt",
                "structure": "./prompts/part1_structure.txt",
                "vocab": "./prompts/part1_vocabulary.txt"},
    "part_3" : {"grammar": "./prompts/part3_grammar.txt",
                "structure": "./prompts/part3_structure.txt",
                "vocab": "./prompts/part3_vocabulary.txt"},
    "part_2" : {"grammar": "./prompts/part2_general.txt",
                "structure": "./prompts/part2_structure.txt",
                "vocab": "./prompts/part2_recs.txt"}
}

def get_prompt_from_file(level, part, feed_type):
    feed_part = f"part_{part}"
    if level == 0:
        l_file= feedback_type_local[feed_part][feed_type]
        # if part == 1:
        #     DATABASE_ID = "4d21f756a96f4a9ea0686ed3c3148f58"
        # else:
        #     DATABASE_ID = "3b73852365ab451d9aa62481900ea72a"
    elif level == 1:
        l_file = feedback_type_local[feed_part][feed_type]
    else:
        l_file = "./prompts/general.txt"

    with open(l_file) as f:
        prompt = f.read()
    return prompt

def get_prompt(level, part, feed_type):
    TOKEN = os.environ["NOTION_TOKEN"]
    feed_part = f"part_{part}"
    if level == 0:
        DATABASE_ID = feedback_type[feed_part][feed_type]
        # if part == 1:
        #     DATABASE_ID = "4d21f756a96f4a9ea0686ed3c3148f58"
        # else:
        #     DATABASE_ID = "3b73852365ab451d9aa62481900ea72a"
    elif level == 1:
        DATABASE_ID = feedback_type[feed_part][feed_type]
    else:
        DATABASE_ID = "5d220283b9884435b3fc6fc6bcf11418"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    prompt_list = []
    url = f"https://api.notion.com/v1/blocks/{DATABASE_ID}/children"

    j = 1
    response = requests.get(url, headers=headers)
    data = response.json()
    for result in range(len(data["results"])):
        type = data["results"][result]["type"]
        for i in range(len(data["results"][result][type]["rich_text"])):
            text = data["results"][result][type]["rich_text"][i]["text"]["content"]
            if data["results"][result][type]["rich_text"][i]["annotations"]["bold"]:
                text = f"**{text}**"
            if type == "numbered_list_item":
                text = f"{j}. {text}"
                j += 1
            else:
                j = 1

            prompt_list.append(text.strip())

    # print(data["results"][3])
    return prompt_list


def generate_feedback(temperature, text, level, part, feed_type):
    band = -1
    if os.environ["ENV"] == "DEV":
        system_prompt = "\n".join(get_prompt(level=level, part=part, feed_type=feed_type))
    else:
        system_prompt = get_prompt_from_file(level=level, part=part, feed_type=feed_type)
    overall_prompt = '''
                    As an expert IELTS speaking examiner, your objective is to evaluate a candidate's response to an IELTS Speaking test, adhering to IELTS standards, and provide a overall band score. The prompt should follow the provided input and output formats, focusing on specific criteria and constraints. Here is the optimized prompt:**Your role: Expert IELTS Speaking Examiner****Objective:**Evaluate a candidate's response to an IELTS Speaking test, adhering to IELTS standards, and provide overall band score without further explanation.**Input Format:**Question: [Question provided to the candidate]Answer: [The candidate's answer to the question]**Output Format :**Overall Band Score: Single float type overall score**Evaluation Process:**1. Conduct a thorough evaluation based on IELTS criteria.2. Pay attention to task achievement, fluency and coherence, lexical resource and grammatical range and accuracy.**Key Aspects and Constraints:**1. Strict adherence to IELTS evaluation criteria and core values.
                    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    if level == 2:
        overall_score = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-1106:personal::8aoeY77v",
            temperature=temperature,
            messages=[
                {"role": "system", "content": overall_prompt},
                {"role": "user", "content": text},
            ],
        )
        
        band = int(float(overall_score.choices[0].message.content.split(':')[1].strip()))
    logger.info(response)
    
    return (response.choices[0].message.content, band)


class Feedback(feedback_service_pb2_grpc.FeedbackServicer):
    def __init__(self) -> None:
        class Servicer(feedback_service_pb2_grpc.FeedbackServicer):
            def __init__(self) -> None:
                super().__init__()

            def get_feedback(self, request, context):
                logging.info(request.text)
                gpt_feedback, score = generate_feedback(temperature=0.4, text=request.text, level=request.level, part=request.part, feed_type=request.feed_type)
                gpt_feedback = gpt_feedback.replace('"', '\'')
                gpt_feedback = gpt_feedback + "\n"
                # gpt_feedback = gpt_feedback.splitlines(True)[0].split(" ")[1]
                return feedback_service_pb2.FeedbackResponse(
                    band=score, feedback=gpt_feedback
                )

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        feedback_service_pb2_grpc.add_FeedbackServicer_to_server(
            Servicer(), self.server
        )

    def start(self, port):
        self.server.add_insecure_port(f"[::]:{port}")
        self.server.start()

        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            self.server.stop(0)


Feedback().start(50052)