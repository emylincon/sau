#!/bin/python3
import time
import logging
from logging import handlers
import sys
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
import prometheus_client
from argparse import ArgumentParser
import yaml
import boto3
import multiprocessing
import sys
import platform
import json
from info import VERSION, BUILD_DATE, AUTHOR
from multiprocessing_logging import install_mp_handler


class Log:
    """
    A class for configuring and managing logging in the SAU Exporter.

    Attributes:
    - level (str): The logging level (default: "info").
    - path (str): The directory where the log file will be stored (default: current directory).
    - retention (int): Number of backup log files to keep (default: 7).

    Methods:
    - setlogger(): Configures and sets up the logger with specified settings.

    """

    def __init__(
        self, level: str = "info", path: str = ".", rentention: int = 7
    ) -> None:
        """
        Initializes a new Log instance.

        Args:
        - level (str): The logging level (default: "info").
        - path (str): The directory where the log file will be stored (default: current directory).
        - retention (int): Number of backup log files to keep (default: 7).

        Returns:
        None

        """
        self.level = level
        self.path = path
        self.retention = rentention

    def setlogger(self) -> None:
        """
        Configures and sets up the logger with the specified settings.

        Returns:
        None

        """
        levels: dict = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARNING,
            "error": logging.ERROR,
        }
        logfile = f"{self.path}/sau_exporter.log"
        # logger = logging.getLogger("sau_exporter")
        loglevel = levels.get(self.level.lower(), logging.INFO)
        format = 'time=%(asctime)s pid=%(process)d level=%(levelname)-2s message="%(message)s"'
        formatter = logging.Formatter(format)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)

        file_handler = handlers.TimedRotatingFileHandler(
            logfile, when="midnight", backupCount=self.retention
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logging.basicConfig(
            format='time=%(asctime)s pid=%(process)d level=%(levelname)-2s message="%(message)s"',
            level=loglevel,
            handlers=[file_handler, stdout_handler],
        )


class EC2SAUCollector(Log):
    """
    Collector class used to scrape EC2 and EBS volume data.

    Attributes:
    - regions (list): List of AWS regions to collect metrics from.
    - level (str): The logging level (default: "info").
    - path (str): The directory where the log file will be stored (default: current directory).
    - retention (int): Number of backup log files to keep (default: 7).

    Methods:
    - get_stopped_ec2(region: str) -> list: Retrieves stopped EC2 instances for a given region.
    - get_unattached_volumes(region: str) -> dict: Retrieves unattached EBS volumes in the specified AWS region.
    - get_instance_metrics() -> dict: Retrieves metrics related to instances and volumes in different regions.

    """

    def __init__(
        self, regions: list, level: str = "info", path: str = ".", rentention: int = 7
    ) -> None:
        """
        Initializes a new EC2SAUCollector instance.

        Args:
        - regions (list): List of AWS regions to collect metrics from.
        - level (str): The logging level (default: "info").
        - path (str): The directory where the log file will be stored (default: current directory).
        - retention (int): Number of backup log files to keep (default: 7).

        Returns:
        None

        """
        Log.__init__(self, level=level, path=path, rentention=rentention)
        self.regions = regions

    def get_stopped_ec2(self, region: str) -> list:
        """_summary_
        Gets all stopped ec2 instances for a given region

        Args:
            region (str): aws region to query

        Returns:
            list: returns a list of all stopped ec2 instances
        """
        self.setlogger()
        logging.debug("get_stopped_ec2 for region %s", region)
        client = boto3.client("ec2", region_name=region)
        result = []
        filter = [{"Name": "instance-state-name", "Values": ["stopped"]}]
        try:
            response = client.describe_instances(Filters=filter)
            for instance in response["Reservations"]:
                tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
                item = {
                    "name": tags.get("Name"),
                    "region": instance["Placement"]["AvailabilityZone"],
                    "instanceid": instance["InstanceId"],
                    "region": region,
                }
                result.append(item)
            client.close()
            return result
        except Exception as error:
            logging.error(f"error retrieving stopped ec2 instances from AWS: {error}")
            return result

    def get_unattached_volumes(self, region: str) -> dict:
        """_summary_
        Retrieves unattached volumes in the specified AWS region.

        Args:
            self: The current instance.
            region (str): The AWS region where the volumes are located.

        Returns:
            dict: A dictionary containing two keys:
                - 'states' (dict): A dictionary containing the count of volumes in different states.
                  Possible states are 'unattached' and 'error'.
                - 'result' (list): A list of dictionaries, where each dictionary represents an unattached
                  volume with the following keys:
                    - 'name' (str): The name of the volume.
                    - 'availabilityzone' (str): The availability zone of the volume.
                    - 'size' (str): The size of the volume in the format '{size}GB'.
                    - 'volumeid' (str): The ID of the volume.
                    - 'volumetype' (str): The type of the volume.
                    - 'state' (str): The state of the volume, which can be 'unattached' or an 'error' state.
                    - 'region' (str): The AWS region where the volume is located.

        Raises:
            None

        """

        self.setlogger()
        logging.debug("get_unattached_volumes for region %s", region)
        client = boto3.client("ec2", region_name=region)
        result = []
        states = {"unattached": 0, "error": 0}
        filter = [{"Name": "status", "Values": ["available", "error"]}]
        try:
            response = client.describe_volumes(Filters=filter)
            for volume in response["Volumes"]:
                tags = {tag["Key"]: tag["Value"] for tag in volume.get("Tags", [])}
                state = (
                    "unattached" if volume["State"] == "available" else volume["State"]
                )
                states[state] += 1
                item = {
                    "name": tags.get("Name"),
                    "availabilityzone": volume["AvailabilityZone"],
                    "size": f'{volume["Size"]}GB',
                    "volumeid": volume["VolumeId"],
                    "volumetype": volume["VolumeType"],
                    "state": state,
                    "region": region,
                }
                result.append(item)
            client.close()
            return {"states": states, "result": result}
        except Exception as error:
            logging.error(f"error retrieving volume details from AWS: {error}")
            return {"states": states, "result": []}

    def get_instance_metrics(self) -> dict:
        """_summary_
        Retrieves metrics related to instances and volumes in different regions.

        Args:
            self: The current instance.

        Returns:
        dict: A dictionary containing the following metrics:
            - 'stopped_instances' (list): List of stopped instances.
            - 'volumes' (list): List of volumes.
            - 'volume_states' (dict): Dictionary with the following keys:
                - 'unattached' (int): Number of unattached volumes.
                - 'error' (int): Number of volumes with errors.

        Raises:
        Exception: If an error occurs during the retrieval process.

        """
        result = {
            "stopped_instances": [],
            "volumes": [],
            "volume_states": {"unattached": 0, "error": 0},
        }
        processes = []
        funcs = {"ec2": self.get_stopped_ec2, "volume": self.get_unattached_volumes}
        pool = multiprocessing.Pool()

        for region in self.regions:
            for name, func in funcs.items():
                logging.debug("calling func for region %s", region)
                processes.append(
                    {
                        "name": name,
                        "process": pool.apply_async(func=func, kwds={"region": region}),
                    }
                )

        for p in processes:
            if p["name"] == "ec2":
                result["stopped_instances"] += p["process"].get()
            else:
                response = p["process"].get()
                result["volumes"] += response["result"]
                for key in result["volume_states"]:
                    result["volume_states"][key] += response["states"][key]
        return result

    def collect(self):
        """_summary_
        Collects various metrics related to EC2 instances and EBS volumes and yields them for monitoring.

        Args:
            self: The current instance.

        Yields:
        Generator: Yields metric data for monitoring.

        Raises:
        Exception: If an error occurs during the collection process.

        """
        logging.info("Collecting metrics...")
        data = self.get_instance_metrics()

        # compose metrics for stopped ec2 instances total
        stopped = data["stopped_instances"]
        gauge = GaugeMetricFamily(
            name=f"sau_ec2_stopped_instances_total",
            documentation=f"EC2 stopped instances total",
        )
        gauge.add_metric(labels=[], value=len(stopped))
        yield gauge

        # compose metrics for stopped ec2 instances
        if stopped:
            gauge = GaugeMetricFamily(
                name=f"sau_ec2_stopped_instances",
                documentation=f"EC2 stopped instances",
                labels=list(stopped[0].keys()),
            )
            for instance in stopped:
                gauge.add_metric(labels=list(instance.values()), value=1)
            yield gauge

        # compose metrics for ebs volumes total
        states = data["volume_states"]
        gauge = GaugeMetricFamily(
            name=f"sau_ebs_volumes_total",
            documentation=f"EC2 EBS volumes total unattached or error",
            labels=list(states.keys()),
        )
        for key, value in states.items():
            gauge.add_metric(labels=[key], value=value)
        yield gauge

        # compose metrics for ebs volumes
        volumes = data["volumes"]
        if volumes:
            gauge = GaugeMetricFamily(
                name=f"sau_ebs_volumes",
                documentation=f"EC2 EBS volumes unattached or error",
                labels=list(volumes[0].keys()),
            )
            for volume in volumes:
                gauge.add_metric(labels=list(volume.values()), value=1)
            yield gauge
        logging.info("metrics successfully collected")


class Util(Log):
    """Utility class for a collection of utility functions.

    Attributes:
        default_exporter_port (int): Default port for the exporter.
        default_logging (dict): Default logging configuration.

    Methods:
        __init__(self, level: str = "info", path: str = ".", rentention: int = 7) -> None:
            Initializes the Util class.

        getlogger(level: str = "info", path: str = ".", backupCount: int = 7) -> logging.Logger:
            Set up and configure a logger for the sau_exporter.

        loop_until_interrupt() -> None:
            Executes a loop until an interrupt signal is received and then shuts down the SAU exporter.

        read_yaml_file(filename: str) -> dict:
            Read a YAML file and return its contents as a dictionary.

        get_config(filename: str) -> dict:
            Retrieves the configuration from a YAML file and performs necessary checks and adjustments.

        version() -> str:
            Retrieves version information about the application.

    """

    default_exporter_port = 9191
    default_logging = {"retention": 7, "directory": ".", "level": "info"}

    def __init__(
        self, level: str = "info", path: str = ".", rentention: int = 7
    ) -> None:
        Log.__init__(self, level=level, path=path, rentention=rentention)

    @staticmethod
    def getlogger(
        level: str = "info", path: str = ".", backupCount: int = 7
    ) -> logging.Logger:
        """
        Set up and configure a logger for the sau_exporter.

        Args:
        level (str): Logging level. Defaults to "info".
        path (str): Path where the log file will be stored. Defaults to the current directory.
        backupCount (int): Number of backup log files to keep. Defaults to 7.

        Returns:
        Logger: Configured logger for the sau_exporter.

        """
        levels: dict = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARNING,
            "error": logging.ERROR,
        }
        path = f"{path}/sau_exporter.log"
        logger = logging.getLogger("sau_exporter")
        logger.setLevel(levels.get(level.lower(), logging.INFO))
        format = 'time=%(asctime)s pid=%(process)d level=%(levelname)-2s message="%(message)s"'
        formatter = logging.Formatter(format)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)

        file_handler = handlers.TimedRotatingFileHandler(
            path, when="midnight", backupCount=backupCount
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)
        return logger

    @staticmethod
    def loop_until_interrupt():
        """
        Executes a loop until an interrupt signal is received and then shuts down the SAU exporter.

        Returns:
        None

        """
        try:
            while True:
                time.sleep(100)
        except KeyboardInterrupt:
            logging.info("Shutting down SAU exporter")
            sys.exit(0)

    @staticmethod
    def read_yaml_file(filename: str) -> dict:
        """
        Read a YAML file and return its contents as a dictionary.

        Args:
        filename (str): The path to the YAML file.

        Returns:
        dict: The contents of the YAML file as a dictionary.

        Raises:
        FileNotFoundError: If the specified file is not found.
        yaml.YAMLError: If an error occurs during the YAML file reading process.

        """
        try:
            with open(filename, "r") as stream:
                return yaml.safe_load(stream)
        except FileNotFoundError as error:
            logging.error("config File not found: %s" % filename)
            sys.exit(1)
        except yaml.YAMLError as error:
            logging.error(f"error reading file {filename}: {error}")
            return {}

    def get_config(filename: str) -> dict:
        """
        Retrieves the configuration from a YAML file and performs necessary checks and adjustments.

        Args:
        filename (str): The path to the YAML configuration file.

        Returns:
        dict: The processed configuration as a dictionary.

        Raises:
        ValueError: If 'regions' are not specified in the configuration file.

        """
        if not filename:
            raise ValueError("The configuration file must be specified")
        config = Util.read_yaml_file(filename)
        if not config.get("regions", []):
            raise ValueError(
                f"regions must be specified in the configuration file {filename}"
            )
        if not config.get("exporter_port"):
            config["exporter_port"] = 9191
        Util.default_logging.update(config.get("logging", {}))
        config["logging"] = Util.default_logging
        return config

    def version() -> str:
        """
        Retrieves version information about the application.

        Returns:
        str: A JSON-formatted string containing version information, build date, author, Python version, and OS platform.

        """
        info = {
            "version": VERSION,
            "buildDate": BUILD_DATE,
            "author": AUTHOR,
            "pythonVersion": sys.version,
            "OSPlatform": platform.platform(),
        }
        return json.dumps(info, sort_keys=True)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="SaU exporter",
        description="AWS EC2 Stopped and Unattached (SaU) volumes exporter ",
        epilog="Created by Emeka Ugwuanyi © 2023",
    )

    parser.add_argument("-c", "--configfile", help="config file path", type=str)

    parser.add_argument("-v", "--version", action="version", version=Util.version())

    args = parser.parse_args()

    # Global variable
    CONFIG_FILE = args.configfile

    config = Util.get_config(filename=CONFIG_FILE)

    # Remove default metrics
    prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
    prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
    prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

    util = Util(
        path=config["logging"]["directory"],
        rentention=config["logging"]["retention"],
        level=config["logging"]["level"],
    )
    util.setlogger()

    install_mp_handler()

    # Create exporter logger
    Logging = Util.getlogger(
        path=config["logging"]["directory"], backupCount=config["logging"]["retention"]
    )

    logging.info("Starting SAU Exporter")

    # Starts a WSGI server for prometheus metrics as a daemon thread
    start_http_server(port=config["exporter_port"], addr="0.0.0.0")

    logging.info(f"config: {config}")

    # Add EC2SAUCollector to prometheus registry
    REGISTRY.register(
        EC2SAUCollector(
            regions=config["regions"],
            path=config["logging"]["directory"],
            rentention=config["logging"]["retention"],
            level=config["logging"]["level"],
        )
    )

    logging.info(
        f"SAU Exporter started. Metrics path: http://localhost:{config['exporter_port']}/"
    )

    # Keep main thread active
    Util.loop_until_interrupt()
