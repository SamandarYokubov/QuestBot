from typing import Annotated
import logging
import os
import json

from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder

from client import FileClient
from client_writing import ClientWriting
from .utils import parse_results, get_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(fmt="%(levelname)s %(asctime)s %(module)s %(filename)s %(lineno)s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


app = FastAPI()
# ss

@app.post("/generate_next_question/")
async def generate_question(sid: str, previous_questions_and_answers: list, next_question: str):
    response = await get_response(previous_questions_and_answers=previous_questions_and_answers, new_question=next_question)
    return response

@app.post("/writing/")
async def send_writing(sid: str, part_no: int, essay_prompt: str, essay: str, essay_img: UploadFile | None = None):
    client_w = ClientWriting("writing:50055")
    if part_no == 1:
    
        response = client_w.get_feedback_writing(essay, part_no, sid, essay_prompt, essay_img.read())
    else:
        response = client_w.get_feedback_writing(essay, part_no, sid, essay_prompt, b'')
    return Response(content=response.feedback, media_type="application/json")


@app.post("/speaking/")
async def create_upload_file(sid: str, part_no: int = None, question: str = None, question_no: int = None, file: UploadFile | None = None, get_result: bool = False):
    cl = FileClient(os.environ["PORT"])
    if file:
        response = cl.upload_data(sid=sid, part_no=part_no, question=question, q_no=question_no, in_file=file.file.read(), get_result=get_result)
    else:
        response = cl.upload_data(sid=sid, part_no=part_no, question=question, q_no=question_no, in_file=b'', get_result=get_result)
    if response.band == 200:
        logger.info(response.feedback)
        # return response.feedback
        return 200
    else:
        logger.info(response)
        data = await parse_results(response.feedback)
        logger.info(data)
        # data = data.update({"sid": sid})
        # logger.info(data)
        # return json.dumps(data)
        
        return Response(content=json.dumps(data), media_type="application/json")