from typing import Annotated
import logging
import os
import json

from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, Response

from client import Client
from utils import parse_as_json



logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(fmt="%(levelname)s %(asctime)s %(module)s %(filename)s %(lineno)s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


app = FastAPI()


@app.post("/generate_questions/")
async def generate_questions(id: str, course_name: str, course_module: int, question_type: str, content_type: str):
    cl = Client("quest_gen:50052")
    
    response = cl.call_server(user_id=id, course_name=course_name, course_module=course_module, question_type=question_type, content_type=content_type)

    logger.info(response.questions)
    data = await parse_as_json(response.questions)
    logger.info(data)
    return Response(content=json.dumps(data), media_type="application/json")
