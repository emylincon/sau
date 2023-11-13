# SAU Exporter
## Overview

The SAU Exporter is a Python-based application designed to collect and expose AWS EC2 and EBS volume metrics for monitoring and observability. It utilizes the Prometheus client library to provide an HTTP endpoint for scraping metrics.

## Features
* **EC2 Metrics**: Collects information about stopped EC2 instances in different AWS regions.
* **EBS Volume Metrics**: Retrieves data on unattached/errored EBS volumes, including volume state, type, size, and region.
* **Prometheus Integration**: Exposes metrics in the Prometheus format, making it compatible with Prometheus monitoring systems.

# Getting Started

## Installing via pip
Offers support for python>=3.8
```bash
pip install sau
```
### Using pip package after installation
```bash
python3 -m sau -c /path/to/config.yaml
```

## Installing using docker
The docker repository is available at [link](https://hub.docker.com/repository/docker/ugwuanyi/sau/general). You will need the following:
* **config file**: [see section](#configuration)
* **AWS Credentials**: It would be easier to put the creds in a env file and reference the file when running container. Example `.env` file can be seen below:
```env
AWS_ACCESS_KEY_ID=129QJDNC2OQD09N
AWS_SECRET_ACCESS_KEY=9KXXXXXXXXX
AWS_REGION=eu-central-1
```
To run the container, use the example command below:
```bash
docker run -ti --env-file .env -v /path/to/config.yaml:/sau/config.yaml ugwuanyi/sau:latest -c /sau/config.yaml
```

### Prerequisites:
* Python 3.8+ installed on your system.
* Ensure the required Python libraries are installed by running the following command.
```bash
pip install -r requirements.txt
```

### Configuration:
Create a YAML configuration file with the necessary settings.
#### Configuration Options
* **Regions**: Specify the AWS regions for which you want to collect metrics.
* **Exporter Port**: Define the port on which the exporter will expose metrics (default: 9000).
* **Logging Configuration**: Customize logging settings, such as log file directory and retention.
See example below.
```yaml
# list of regions to scrape: REQUIRED
regions:
  - eu-central-1
  - eu-west-1

# exporter port. Defaults to 9000
exporter_port: 9000

# Logging configuration
logging:
  # Number of log files to retain after log rotation
  retention: 7
  # log directory. defaults to current working directory
  directory: "."
  # log level (debug, info, warn, error). Defaults to info
  level: info
```

### Running the Exporter:
Execute the exporter by providing the path to the configuration file:

```bash
python3 sau_exporter.py -c /path/to/your/config.yaml
```

#### Metrics Endpoint:
Once the exporter is running, metrics can be accessed at `http://localhost:<exporter_port>/`.

## Customization
Feel free to extend or customize the exporter to meet your specific requirements. You can modify the provided code or add additional collectors to gather more AWS resource metrics.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it according to the terms of the license.

## Author
Created by Emeka Ugwuanyi. For questions or feedback, please contact me.


**Happy monitoring!**
