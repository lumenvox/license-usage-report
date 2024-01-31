# usage_report.py
# Simple script to run the UsageReport function of the Reporting API
# Attach the component name as a final argument.
#
# Be sure to have generated Protocol Buffer files in the same directory, as this script uses them as imports to function

import sys
import grpc
import lumenvox.api.reporting_pb2 as reporting_api
from lumenvox.api.reporting_pb2_grpc import ReportingAPIServiceStub


def usage_report(metadata, reporting_stub, component: str = '') -> reporting_api.UsageReportResponse:
    """
    UsageReport function from reporting.proto
    metadata: Tuple containing deployment and operator id
    component: The component to return. Note that if specified, it will return info only for that component
    """
    req = reporting_api.UsageReportRequest(component=component)
    usage_report_response: reporting_api.UsageReportResponse = reporting_stub.UsageReport(req, metadata=metadata)

    return usage_report_response


if __name__ == "__main__":
    # sys.argv[1] - IP address and port (ex. 127.0.0.1:8090)
    # sys.argv[2] - deployment ID
    # sys.argv[3] - operator ID
    # sys.argv[4] - component

    arg_count = len(sys.argv)

    if arg_count < 4:
        print('Invalid number of arguments, got', arg_count)
        print('python usage_report.py [ip:port] [deployment ID] [operator ID] [optional component]')
        print('For example...')
        print('python usage_report.py 127.0.0.1:8090 ffab528a-63d0-4da4-a56b-49564e2ff6bc 42812fb3-0060-471e-b7a8-6e744c083318')
        print('or...')
        print('python usage_report.py aether-dev.lumenvox.com:8090 ffab528a-63d0-4da4-a56b-49564e2ff6bc 42812fb3-0060-471e-b7a8-6e744c083318')
        sys.exit(2)

    reporting_api_service = str(sys.argv[1])  # IP and port of reporting service
    metadata = ()
    metadata += (("x-deployment-id", str(sys.argv[2])),)
    metadata += (("x-operator-id", str(sys.argv[3])),)

    max_message_mb = 4

    channel = grpc.insecure_channel(reporting_api_service,
                                    options=[
                                        ('grpc.max_send_message_length', max_message_mb * 1048576),
                                        ('grpc.max_receive_message_length', max_message_mb * 1048576),
                                    ])

    reporting_stub = ReportingAPIServiceStub(channel)

    print(usage_report(metadata=metadata, reporting_stub=reporting_stub))
