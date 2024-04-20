import logging
import time
import os
from concurrent import futures
from celery import group
from celery.result import AsyncResult
import grpc
from uuid import uuid4
from client import FeedbackClient
from generated_code.stt import stt_pb2, stt_pb2_grpc
from pythonjsonlogger import jsonlogger
from tasks import get_data, transcribe, exists, append2list, get_feedback, execute_sequential, get_transcriptions, get_feedback_individual

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt="%(levelname)s %(asctime)s %(module)s %(filename)s %(lineno)s %(message)s"
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


class TranscribeAndFeedback(stt_pb2_grpc.TranscribeAndFeedbackServicer):
    def __init__(self) -> None:
        class Servicer(stt_pb2_grpc.TranscribeAndFeedbackServicer):
            def __init__(self) -> None:
                super().__init__()

            def data_upload(self, request, context):
                sid = request.sid
                # task_id = uuid4()
               
                result = execute_sequential(request.file, request.question, request.q_id, sid, request.part_number, get_result=request.get_result)
                # status = AsyncResult(task_id)
                if result == 1:
                    append2list(sid)
                    all_feedback = get_data(sid, delete=True)
                    all_feedback = all_feedback[:len(all_feedback)-1]
                    return stt_pb2.ResultResponse(band=0, feedback=all_feedback)
                while(not result.ready()):
                    time.sleep(0.5)
                return stt_pb2.ResultResponse(band=200, feedback=get_transcriptions(sid))

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        stt_pb2_grpc.add_TranscribeAndFeedbackServicer_to_server(
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


TranscribeAndFeedback().start(50051)