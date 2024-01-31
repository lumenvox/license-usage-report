### Usage Report Script
#### `usage_report.py`

A simple script that takes the IP address and port of the reporting API service, deployment ID, operator ID, and an 
option component name as arguments.
Example:

```shell
# py usage_report.py [ip:port] [deployment ID] [operator ID] [optional component name]
```

Running the script will print UsageReport output. 

Be sure to have generated Protocol Buffer files in the same directory (there should be a `lumenvox` directory with 
generated `_pb2.py` and `_pb2_grpc.py`) upon running, as this script uses them as imports to function.

You may need to install the protoc tool to your machine to enable this compilation.

The stub files will be generated in `google` and `lumenvox` folders from the project root.

## Setup

Copy the provided folder in any location.  
Install python >=3.9  
be sure that opening the command line and executing python, it will properly reply, otherwise add Python installation path in your %PATH%  
install the required module as in follows:  
``
$ python -m pip install grpcio  
$ python -m pip install grpcio-tools  
``  

cd to <your location>  
execute the command to generate the report described above. 
