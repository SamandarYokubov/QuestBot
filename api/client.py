import grpc
import time

from generated_code import quest_service_pb2_grpc, quest_service_pb2


class Client:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = quest_service_pb2_grpc.QuestServiceStub(channel)

    def call_server(self, user_id: str, course_name: str, course_module: int, question_type: str, content_type: str):
        request = quest_service_pb2.Request(user_id=user_id, course_name=course_name, course_module=course_module, question_type=question_type, content_type=content_type)
        response = self.stub.get_questions(request)
        
        return response
