
from openai import OpenAI
import os
import logging
# import requests
from pythonjsonlogger import jsonlogger

import grpc
from generated_code import quest_service_pb2
from generated_code import quest_service_pb2_grpc
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


question_type_local = {
    "short_answer": "./prompts/short_answer.txt",
    "multiple_choice": "./prompts/multiple_choice.txt"
}

def get_prompt_from_file(question_type):
    l_file = question_type_local[question_type]


    with open(l_file) as f:
        prompt = f.read()
    return prompt



def generate_questions(temperature, text, question_type, number_of_questions=10):
    
    system_prompt = get_prompt_from_file(question_type=question_type)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    
    logger.info(response)
    
    return (response.choices[0].message.content)


class QuestService(quest_service_pb2_grpc.QuestServiceServicer):
    def __init__(self) -> None:
        class Servicer(quest_service_pb2_grpc.QuestServiceServicer):
            def __init__(self) -> None:
                super().__init__()

            def get_questions(self, request, context):
                # logging.info(request.text)
                # gpt_feedback, score = generate_feedback(temperature=0.4, text=request.text, level=request.level, part=request.part, feed_type=request.feed_type)
                # gpt_feedback = gpt_feedback.replace('"', '\'')
                # gpt_feedback = gpt_feedback + "\n"
                # gpt_feedback = gpt_feedback.splitlines(True)[0].split(" ")[1]
                return quest_service_pb2.Response(
                    questions="hfgfghjhgjk"
                )

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        quest_service_pb2_grpc.add_QuestServiceServicer_to_server(
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


QuestService().start(50052)