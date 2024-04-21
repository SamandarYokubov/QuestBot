# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import quest_service_pb2 as quest__service__pb2


class QuestServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_questions = channel.unary_unary(
                '/QuestService/get_questions',
                request_serializer=quest__service__pb2.Request.SerializeToString,
                response_deserializer=quest__service__pb2.Response.FromString,
                )


class QuestServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_questions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QuestServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_questions': grpc.unary_unary_rpc_method_handler(
                    servicer.get_questions,
                    request_deserializer=quest__service__pb2.Request.FromString,
                    response_serializer=quest__service__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'QuestService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class QuestService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_questions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/QuestService/get_questions',
            quest__service__pb2.Request.SerializeToString,
            quest__service__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)