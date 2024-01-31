# Get Usage Report Test App

To configure this project, you need to have a recent version of Python (>= 3.9)
installed, and you need to create a virtual environment in your project
folder, i.e.:

```shell
python -m venv venv
```

You should also activate the `venv` environment (should be automatic if using
PyCharm) 

### Windows
```shell
venv\Scripts\activate.bat
```

### Linux (or WSL)
```shell
source ./venv/bin/activate
```

## Install Requirements

To install the required packages that are described in `requirements.txt`, use
the following (Windows or Linux after venv is activated):
```shell
pip -r requirements.txt
```

## Version Specific

Note that the behavior or the API changed dramatically between version 3.4
and 4.0

## API Version 4.0 and later

In order to run tests against version 4.0, you need to generate the proto
files for the version of Python you are using:

```shell
python importer.py
```

### Run Usage Report

Once the above is completed, there should be `/lumenvox` and `/google` in
the project root folder, so you can now run the test code, for example:

```shell
python usage_report.py <api-ip-address>:<api-port> <deployment-id> <operator-id>
```

The result may look something like this:
```shell
session_ms: 41193
session_audio_ms: 131393
license_usage {
  key: "VAD"
  value {
    usage_count: 8
    usage_ms: 43198
  }
}
license_usage {
  key: "SESSION_USAGE"
  value {
    usage_count: 16
    usage_ms: 41193
  }
}
license_usage {
  key: "INTERACTION_USAGE"
  value {
    usage_count: 16
    usage_ms: 39518
  }
}
license_usage {
  key: "ASR_ENUS"
  value {
    usage_count: 14
    usage_ms: 71612
  }
}
license_usage {
  key: "ASR_ENUS_50"
  value {
    usage_count: 14
    usage_ms: 71612
  }
}
```
