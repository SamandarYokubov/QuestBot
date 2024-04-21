from celery import Celery #type: ignore
from celery import chain, group
from celery.result import GroupResult
from openai import OpenAI
import os
import redis
from client import FeedbackClient
import time
import json
import logging
import typing

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client_ = OpenAI(api_key=os.environ["API"])
red = redis.Redis(os.environ["REDIS_CACHE"], db=1, decode_responses=True)
celery = Celery('tasks', broker=os.environ["CELERY_BROKER_URL"], backend=os.environ["CELERY_BACKEND_URL"])


def execute_sequential(audio_file, question, question_no, sid, part_no, level=0, get_result=False):
    logger.info(get_result)
    
    
    result = (transcribe.s(audio_file, question, 0, sid, part_no) | get_feedback.s(0, sid, part_no, level=1, feed_type="grammar")).apply_async()
    logger.info(result)
    return result.parent


@celery.task
def transcribe(audio_file, question, question_no, sid, part_no):
    if question_no == 1:
        red.delete(sid)
        red.delete(f'{sid}:result')
    with open('/tmp/test1.m4a', "wb") as binary_file:
        binary_file.write(audio_file)
        # shutil.copyfile(request.file,'/tmp/test1.mp4')
        audio = open('/tmp/test1.m4a', "rb")
        try:
            transcript = client_.audio.transcriptions.create(
                        model="whisper-1",
                        language="en",
                        file=audio, 
                        response_format="text"
                        )
        except Exception:
            transcript = "empty text"
    data = f"QUESTION: {question}\nANSWER: {transcript}\n"
    red.set(f'{sid}:trans', data)
    json_str = f'{{"question_no":{question_no}, "question":"{question}", "answer":"{transcript}", "part_no":{part_no}}},'
    
    red.append(sid, json_str)
    red.expire(sid, 3000, nx=True)
    return data

def extract_audio():
    pass

@celery.task
def get_feedback(transcript, question_no, sid, part_no, level, feed_type="NA"):
    # def get_feedback(data: typing.List):
    # transcript, question_no, sid, part_no, level = data[0], data[1], data[2],
    client = FeedbackClient("feedback:50052")
    if level != 0:
        transcript= collect_transcriptions(sid, part_no=part_no, level=level)
    feedback_ = client.get_feedback(transcript, level=level, part=part_no, feed_type=feed_type)
    # feedback = feedback_.feedback.replace('"', '\'')
    if level == 0:
        answer = transcript.split("\n")[1].split(":")[1].strip()
    else:
        answer = "NA"
    json_str = f'{{"question_no":{question_no}, "part_no":{part_no}, "feedback":"{feedback_.feedback}", "level":{level}, "band":{feedback_.band}, "transcript":"{answer}", "feed_type":"{feed_type}"}},'
    red.append(f'{sid}:result', json_str)
    return json_str


def get_data(uid: str, delete: bool=False):
    result = ''
    if delete:
        result = red.get(f'{uid}:result')
        red.delete(f'{uid}:result')
        red.delete(f'{uid}')
        return result
    else:
        result = red.get(uid)
    return result

def exists(uid: str):
    result = get_data(uid)
    data = result[:len(result)-1]
    json_str = f'[{data}]'
    logger.info(data)
    data = json.loads(json_str, strict=False)
    for datum in data:
            if datum["part_no"] == 3:
                return True
    return False

def append2list(sid: str):
    result = get_data(sid)
    ret = red.lpush(f'{sid}:list', result)
    # red.expire(f'{sid}:list', 3600, nx=True)
    logger.info(ret)

def ret_list(sid: str):
    result = red.lindex(f'{sid}:list', 0)
    
    return result

def get_transcriptions(sid):
    return red.get(f'{sid}:trans')

@celery.task
def get_feedback_individual(uid: str, part_no: int|None = None, question_no: int|None = None, level: int = 0, test: bool = False, feed_type="NA"):
    time.sleep(3)
    client = FeedbackClient("feedback:50052")
    
    if test:
        data = ret_list(uid)
    else:
        data = get_data(uid)
    logger.info(data)
    data = data[:len(data)-1]
    json_str = f'[{data}]'
    data = json.loads(json_str, strict=False)
    if question_no:
        response=''
        for datum in data:
            if datum["question_no"] == question_no:
                response = f'QUESTION: {datum["question"]}\nANSWER: {datum["answer"]}\n'
        feedback_ = client.get_feedback(response, level=level, part=part_no, feed_type=feed_type)
        json_str = f'{{"question_no":{question_no}, "part_no":{part_no}, "feedback":"{feedback_.feedback}", "level":0, "feed_type":"{feed_type}"}},'
        red.append(f'{uid}:result', json_str)
    elif part_no:
        response = ''
        for datum in data:
            if datum["part_no"] == part_no:
                response += f'QUESTION: {datum["question"]}\nANSWER: {datum["answer"]}\n'
        feedback_ = client.get_feedback(response, level=level, part=part_no, feed_type=feed_type)
        json_str = f'{{"question_no":0, "part_no":{part_no}, "feedback":"{feedback_.feedback}", "level":1, "feed_type":"{feed_type}"}},'
        red.append(f'{uid}:result', json_str)
    else:
        response = ''
        for datum in data:
            response += f'QUESTION: {datum["question"]}\nANSWER: {datum["answer"]}\n'
        feedback_ = client.get_feedback(response, level=level, part=0, feed_type=feed_type)
        return feedback_.feedback
    # red.expire(f'{uid}:result', 1800, nx=True)
    return 1