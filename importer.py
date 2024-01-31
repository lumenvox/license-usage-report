import os


# THIS IS FOR VERSION 4.0 AND LATER VERSIONS ####

# This will generate the Python stub files needed to connect this app
# to the LumenVox stack using gRPC
#
def import_proto_files():
    # find and import all .proto files in the protobuf folder
    lumenvox_protos = [
        'lumenvox/api/optional_values.proto',
        'lumenvox/api/audio_formats.proto',
        'lumenvox/api/common.proto',
        'lumenvox/api/interaction.proto',
        'lumenvox/api/reporting.proto',
        'lumenvox/api/settings.proto',
        'lumenvox/api/results.proto',
    ]  # Add more proto files to this list as needed

    for proto_input in lumenvox_protos:
        print('Generating stubs for ', proto_input)
        os.system('python -m grpc_tools.protoc -I . -I protobufs '
                  '--python_out=. '
                  '--grpc_python_out=. '
                  '--proto_path=protobufs '
                  '{}'.format(proto_input))

    # Generate/import google proto files
    google_api_protos = [
        'google/protobuf/struct.proto',
        'google/rpc/status.proto'
    ]
    for proto_input in google_api_protos:
        print('Generating stubs for ', proto_input)
        os.system('python -m grpc_tools.protoc -I . -I protobufs '
                  '--python_out=. '
                  '--proto_path=protobufs '
                  '{}'.format(proto_input))


if __name__ == '__main__':
    import_proto_files()
