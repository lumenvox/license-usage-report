""" Usage Report Script
Simple script to run the UsageReport function of the Reporting API.

ex.:
python usage_report.py -i [IP address and port] -d [deployment ID] -o [operator ID] -c [component] -cert [cert. file]

Be sure to have generated Protocol Buffer files in the same directory, as this script uses them as imports to function
"""

import sys
import grpc
import lumenvox.api.reporting_pb2 as reporting_api
from lumenvox.api.reporting_pb2_grpc import ReportingAPIServiceStub


def usage_report(metadata, reporting_stub, component: str = '') -> reporting_api.UsageReportResponse:
    """
    UsageReport function from reporting.proto
    :param reporting_stub: Stub required to access Reporting API RPCs.
    :param metadata: Tuple containing deployment and operator IDs.
    :param component: The component to return. Note that if specified, it will return info only for that component
    :return: UsageReportResponse message (JSON).
    """
    req = reporting_api.UsageReportRequest(component=component)
    usage_report_response: reporting_api.UsageReportResponse = reporting_stub.UsageReport(req, metadata=metadata)

    return usage_report_response


def read_system_arguments(sys_args: list):
    """
    Iterate through list of system arguments and return tuple of the values given.
    :param sys_args: List of system arguments passed from the main function.
    :return: Tuple of fields returned.
    """

    # String values received from system arguments.
    # reporting_api_ip_port, deployment_id and operator_id are required values.
    reporting_api_ip_port = None
    deployment_id = None
    operator_id = None
    component = None
    cert_file = None

    for i in range(len(sys_args)):
        try:
            if (sys_args[i]) == '-i':
                reporting_api_ip_port = str(sys_args[i + 1])
            if sys_args[i] == '-d':
                deployment_id = str(sys_args[i + 1])
            if sys_args[i] == '-o':
                operator_id = str(sys_args[i + 1])
            if sys_args[i] == '-c':
                component = str(sys_args[i + 1])
            if sys_args[i] == '-cert':
                cert_file = str(sys_args[i + 1])
        except IndexError:
            print("Arguments incorrectly formatted.")
            print("python -i [IP address and port] -d [deployment ID] -o [operator ID] -c [component] "
                  "-cert [cert file path]")
            print('For example...')
            print(
                'python usage_report.py -i 127.0.0.1:8090 -d ffab528a-63d0-4da4-a56b-49564e2ff6bc -o '
                '42812fb3-0060-471e-b7a8-6e744c083318')
            print('or...')
            print(
                'python usage_report.py -i aether-dev.lumenvox.com:8090 -d ffab528a-63d0-4da4-a56b-49564e2ff6bc -o '
                '42812fb3-0060-471e-b7a8-6e744c083318')
            sys.exit(2)

    if (not reporting_api_ip_port) or (not deployment_id) or (not operator_id):
        print("Reporting API IP and Port, deployment ID, and operator ID must be provided with the arguments -i, -d, "
              "and -o respectively.")
        sys.exit(2)

    return reporting_api_ip_port, deployment_id, operator_id, component, cert_file


if __name__ == "__main__":
    """
    Usage:
    py usage_report.py -i [IP address and port] -d [deployment ID] -o [operator ID] -c [component] -cert [cert. file]
    """

    argument_values = read_system_arguments(sys_args=sys.argv)

    reporting_api_service = argument_values[0]  # IP and port of reporting service.

    # Set up required user metadata (tuple containing deployment and operator UUIDs).
    user_metadata = ()
    user_metadata += (("x-deployment-id", argument_values[1]),)
    user_metadata += (("x-operator-id", argument_values[2]),)

    max_message_mb = 4

    # Use a secure connection if a cert. file path is provided.
    if argument_values[4] is not None:
        with open(argument_values[4], 'rb') as f:
            credentials = grpc.ssl_channel_credentials(root_certificates=f.read())

            channel = grpc.secure_channel(reporting_api_service,
                                          options=[
                                              ('grpc.max_send_message_length', max_message_mb * 1048576),
                                              ('grpc.max_receive_message_length', max_message_mb * 1048576),
                                          ], credentials=credentials)
    else:
        # Establish channel to allow for API interactions.
        channel = grpc.insecure_channel(reporting_api_service,
                                        options=[
                                            ('grpc.max_send_message_length', max_message_mb * 1048576),
                                            ('grpc.max_receive_message_length', max_message_mb * 1048576),
                                        ])

    # Reference stub from Python code generated from the Protocol Buffer files.
    reporting_api_stub = ReportingAPIServiceStub(channel)

    # Prints the Usage Report response.
    print(usage_report(metadata=user_metadata, reporting_stub=reporting_api_stub, component=argument_values[3]))
