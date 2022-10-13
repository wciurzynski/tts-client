import logging

import techmo_tts_pb2
import techmo_tts_pb2_grpc
import grpc
from create_channel import create_channel


def call_listvoices(args):
    channel = create_channel(args.service, args.tls_directory)
    stub = techmo_tts_pb2_grpc.TTSStub(channel)

    timeout = None
    if args.grpc_timeout > 0:
        timeout = args.grpc_timeout / 1000
    metadata = []
    if args.session_id:
        metadata = [('session_id', args.session_id)]

    request = techmo_tts_pb2.ListVoicesRequest(language=args.language)

    try:
        response = stub.ListVoices(request, timeout=timeout, metadata=metadata)
        print(response)

    except grpc.RpcError as e:
        logging.error("[Server-side error] Received following RPC error from the TTS service:", str(e))


def get_voice_list(args):
    if args.tls_directory:
        channel = create_channel(args.service, args.tls_directory)
    elif hasattr(args, 'root_certificates') and args.root_certificates:
        channel = grpc.secure_channel(args.service, grpc.ssl_channel_credentials(args.root_certificates, args.private_key, args.certificate_chain))
    else:
        channel = grpc.insecure_channel(args.service)

    stub = techmo_tts_pb2_grpc.TTSStub(channel)

    timeout = None
    if args.grpc_timeout > 0:
        timeout = args.grpc_timeout / 1000
    metadata = []
    if args.session_id:
        metadata = [('session_id', args.session_id)]

    request = techmo_tts_pb2.ListVoicesRequest(language=args.language)

    voice_list = list()
    try:
        response = stub.ListVoices(request, timeout=timeout, metadata=metadata)
        for voice in response.voices:
            voice_list.append(voice.voice.name)

    except grpc.RpcError as e:
        logging.error("[Server-side error] Received following RPC error from the TTS service:", str(e))

    return voice_list
