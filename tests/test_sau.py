# -----------------------------------------------------------------------------
# Copyright (c) 2023, Emeka Ugwuanyi.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
#
# -----------------------------------------------------------------------------

#!/bin/python3
import sys
import os
import re
import unittest
import datetime
from typing import Any, List

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, f"{os.path.dirname(os.path.abspath(__file__))}/../src/")

from prometheus_client import generate_latest, make_wsgi_app
from prometheus_client.core import CollectorRegistry

from sau.__main__ import Log, Util, EC2SAUCollector


class MockClient:
    def __init__(self, module: str, region_name: str):
        self.module = module
        self.region_name = region_name

    def describe_instances(self, Filters: List[dict]) -> dict:
        return {
            "Reservations": [
                {
                    "Groups": [],
                    "Instances": [
                        {
                            "AmiLaunchIndex": 0,
                            "ImageId": "ami-0502e817a6212883",
                            "InstanceId": "i-07fb37a99060c44",
                            "InstanceType": "t3.medium",
                            "LaunchTime": "",
                            "Monitoring": {"State": "disabled"},
                            "Placement": {
                                "AvailabilityZone": "eu-central-1a",
                                "GroupName": "",
                                "Tenancy": "default",
                            },
                            "PrivateDnsName": "ip-10-1-1-1.eu-central-1.compute.internal",
                            "PrivateIpAddress": "10.1.1.1",
                            "ProductCodes": [],
                            "PublicDnsName": "",
                            "State": {"Code": 16, "Name": "stopped"},
                            "StateTransitionReason": "",
                            "SubnetId": "subnet-0c4624ba",
                            "VpcId": "vpc-5deb8f",
                            "Architecture": "x86_64",
                            "BlockDeviceMappings": [
                                {
                                    "DeviceName": "/dev/sda1",
                                    "Ebs": {
                                        "AttachTime": "",
                                        "DeleteOnTermination": True,
                                        "Status": "attached",
                                        "VolumeId": "vol-08",
                                    },
                                },
                                {
                                    "DeviceName": "/dev/sdg",
                                    "Ebs": {
                                        "AttachTime": "",
                                        "DeleteOnTermination": False,
                                        "Status": "attached",
                                        "VolumeId": "vol-0d",
                                    },
                                },
                                {
                                    "DeviceName": "/dev/sdh",
                                    "Ebs": {
                                        "AttachTime": "",
                                        "DeleteOnTermination": False,
                                        "Status": "attached",
                                        "VolumeId": "vol-01",
                                    },
                                },
                                {
                                    "DeviceName": "/dev/sdi",
                                    "Ebs": {
                                        "AttachTime": "",
                                        "DeleteOnTermination": False,
                                        "Status": "attached",
                                        "VolumeId": "vol-0a",
                                    },
                                },
                            ],
                            "ClientToken": "",
                            "EbsOptimized": True,
                            "EnaSupport": True,
                            "Hypervisor": "xen",
                            "NetworkInterfaces": [],
                            "RootDeviceName": "/dev/sda1",
                            "RootDeviceType": "ebs",
                            "SourceDestCheck": True,
                            "Tags": [
                                {"Key": "environment", "Value": "development"},
                                {"Key": "Name", "Value": "poc-sau01"},
                            ],
                            "VirtualizationType": "hvm",
                            "CpuOptions": {"CoreCount": 1, "ThreadsPerCore": 2},
                            "CapacityReservationSpecification": {
                                "CapacityReservationPreference": "open"
                            },
                            "HibernationOptions": {"Configured": False},
                            "MetadataOptions": {
                                "State": "applied",
                                "HttpTokens": "optional",
                                "HttpPutResponseHopLimit": 1,
                                "HttpEndpoint": "enabled",
                                "HttpProtocolIpv6": "disabled",
                                "InstanceMetadataTags": "disabled",
                            },
                            "EnclaveOptions": {"Enabled": False},
                            "PlatformDetails": "Linux/UNIX",
                            "UsageOperation": "RunInstances",
                            "UsageOperationUpdateTime": "",
                            "PrivateDnsNameOptions": {},
                            "MaintenanceOptions": {"AutoRecovery": "default"},
                        }
                    ],
                    "OwnerId": "XXXX0000000000000000",
                    "ReservationId": "r-XXX9990001188",
                },
                {
                    "Groups": [],
                    "Instances": [
                        {
                            "AmiLaunchIndex": 0,
                            "ImageId": "ami-0502e817a6212883",
                            "InstanceId": "i-07fb37a99060c44",
                            "InstanceType": "t3.medium",
                            "LaunchTime": "",
                            "Monitoring": {"State": "disabled"},
                            "Placement": {
                                "AvailabilityZone": "eu-central-1a",
                                "GroupName": "",
                                "Tenancy": "default",
                            },
                            "PrivateDnsName": "ip-10-1-1-1.eu-central-1.compute.internal",
                            "PrivateIpAddress": "10.1.1.1",
                            "ProductCodes": [],
                            "PublicDnsName": "",
                            "State": {"Code": 16, "Name": "stopped"},
                            "StateTransitionReason": "",
                            "SubnetId": "subnet-0c4624ba",
                            "VpcId": "vpc-5deb8f",
                            "Architecture": "x86_64",
                            "BlockDeviceMappings": [
                                {
                                    "DeviceName": "/dev/sda1",
                                    "Ebs": {
                                        "AttachTime": "",
                                        "DeleteOnTermination": True,
                                        "Status": "attached",
                                        "VolumeId": "vol-08",
                                    },
                                },
                                {
                                    "DeviceName": "/dev/sdg",
                                    "Ebs": {
                                        "AttachTime": "",
                                        "DeleteOnTermination": False,
                                        "Status": "attached",
                                        "VolumeId": "vol-0d",
                                    },
                                },
                                {
                                    "DeviceName": "/dev/sdh",
                                    "Ebs": {
                                        "AttachTime": "",
                                        "DeleteOnTermination": False,
                                        "Status": "attached",
                                        "VolumeId": "vol-01",
                                    },
                                },
                                {
                                    "DeviceName": "/dev/sdi",
                                    "Ebs": {
                                        "AttachTime": "",
                                        "DeleteOnTermination": False,
                                        "Status": "attached",
                                        "VolumeId": "vol-0a",
                                    },
                                },
                            ],
                            "ClientToken": "",
                            "EbsOptimized": True,
                            "EnaSupport": True,
                            "Hypervisor": "xen",
                            "NetworkInterfaces": [],
                            "RootDeviceName": "/dev/sda1",
                            "RootDeviceType": "ebs",
                            "SourceDestCheck": True,
                            "Tags": [
                                {"Key": "environment", "Value": "stage"},
                                {"Key": "Name", "Value": "poc-sau02"},
                            ],
                            "VirtualizationType": "hvm",
                            "CpuOptions": {"CoreCount": 1, "ThreadsPerCore": 2},
                            "CapacityReservationSpecification": {
                                "CapacityReservationPreference": "open"
                            },
                            "HibernationOptions": {"Configured": False},
                            "MetadataOptions": {
                                "State": "applied",
                                "HttpTokens": "optional",
                                "HttpPutResponseHopLimit": 1,
                                "HttpEndpoint": "enabled",
                                "HttpProtocolIpv6": "disabled",
                                "InstanceMetadataTags": "disabled",
                            },
                            "EnclaveOptions": {"Enabled": False},
                            "PlatformDetails": "Linux/UNIX",
                            "UsageOperation": "RunInstances",
                            "UsageOperationUpdateTime": "",
                            "PrivateDnsNameOptions": {},
                            "MaintenanceOptions": {"AutoRecovery": "default"},
                        }
                    ],
                    "OwnerId": "XXXX0000000000000000",
                    "ReservationId": "r-XXX9990001188",
                },
            ],
            "ResponseMetadata": {
                "RequestId": "3f3a65b7-c0bc-4e38-8487-88ii110990",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "x-amzn-requestid": "3f3a65b7-c0bc-4e38-8487-88ii110990",
                    "cache-control": "no-cache, no-store",
                    "strict-transport-security": "max-age=31536000; includeSubDomains",
                    "vary": "accept-encoding",
                    "content-type": "text/xml;charset=UTF-8",
                    "transfer-encoding": "chunked",
                    "date": "Sun, 27 Oct 2024 17:29:06 GMT",
                    "server": "AmazonEC2",
                },
                "RetryAttempts": 0,
            },
        }

    def describe_volumes(self, Filters: List[dict]) -> dict:
        return {
            "Volumes": [
                {
                    "Attachments": [],
                    "AvailabilityZone": "eu-central-1a",
                    "CreateTime": datetime.datetime(
                        2023,
                        7,
                        11,
                        10,
                        37,
                        35,
                        55000,
                    ),
                    "Encrypted": True,
                    "Size": 20,
                    "SnapshotId": "",
                    "State": "available",
                    "VolumeId": "vol-0c",
                    "Iops": 3000,
                    "Tags": [
                        {"Key": "Name", "Value": "poc-sau-01"},
                        {"Key": "environment", "Value": "dev"},
                    ],
                    "VolumeType": "gp3",
                    "MultiAttachEnabled": False,
                    "Throughput": 125,
                },
                {
                    "Attachments": [],
                    "AvailabilityZone": "eu-central-1a",
                    "CreateTime": datetime.datetime(
                        2023,
                        10,
                        18,
                        9,
                        42,
                        55,
                        860000,
                    ),
                    "Encrypted": True,
                    "Size": 20,
                    "SnapshotId": "",
                    "State": "available",
                    "VolumeId": "vol-0d",
                    "Iops": 3000,
                    "Tags": [
                        {"Key": "environment", "Value": "stage"},
                        {"Key": "Name", "Value": "poc-sau-02"},
                    ],
                    "VolumeType": "gp3",
                    "MultiAttachEnabled": False,
                    "Throughput": 125,
                },
                {
                    "Attachments": [],
                    "AvailabilityZone": "eu-central-1a",
                    "CreateTime": datetime.datetime(
                        2023,
                        10,
                        18,
                        9,
                        42,
                        55,
                        892000,
                    ),
                    "Encrypted": True,
                    "Size": 15,
                    "SnapshotId": "",
                    "State": "available",
                    "VolumeId": "vol-0ef",
                    "Iops": 3000,
                    "Tags": [
                        {"Key": "environment", "Value": "stage"},
                        {"Key": "Name", "Value": "poc-sau-03"},
                    ],
                    "VolumeType": "gp3",
                    "MultiAttachEnabled": False,
                    "Throughput": 125,
                },
            ],
            "ResponseMetadata": {
                "RequestId": "d0651ade-29c1-4999-8b88-98789ij1n2",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "x-amzn-requestid": "d0651ade-29c1-4999-8b88-98789ij1n2",
                    "cache-control": "no-cache, no-store",
                    "strict-transport-security": "max-age=31536000; includeSubDomains",
                    "vary": "accept-encoding",
                    "content-type": "text/xml;charset=UTF-8",
                    "transfer-encoding": "chunked",
                    "date": "Sun, 27 Oct 2024 22:17:30 GMT",
                    "server": "AmazonEC2",
                },
                "RetryAttempts": 0,
            },
        }

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def __enter__(self):
        pass

    def close(self):
        pass


def get_aws_client(module: str, region_name: str) -> Any:
    return MockClient(module, region_name=region_name)


class MockClientWithDottedTags(MockClient):
    """
    Mimics AWS tag keys created by the EBS CSI driver / Kubernetes
    (e.g. `ebs.csi.aws.com/cluster`, `kubernetes.io/created-for/pvc/name`)
    that contain '.' and '/' characters, as described in
    https://github.com/NBCUDTC/nowtv-ansible/issues/9303
    """

    def describe_volumes(self, Filters: List[dict]) -> dict:
        response = super().describe_volumes(Filters=Filters)
        response["Volumes"][0]["Tags"] += [
            {"Key": "ebs.csi.aws.com/cluster", "Value": "true"},
            {"Key": "kubernetes.io/created-for/pvc/name", "Value": "server-data"},
        ]
        return response

    def describe_instances(self, Filters: List[dict]) -> dict:
        response = super().describe_instances(Filters=Filters)
        response["Reservations"][0]["Instances"][0]["Tags"] += [
            {"Key": "ebs.csi.aws.com/cluster", "Value": "true"},
        ]
        return response


def get_aws_client_with_dotted_tags(module: str, region_name: str) -> Any:
    return MockClientWithDottedTags(module, region_name=region_name)


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = Log()
        cls.util = Util()
        cls.regions = ["us-east-1", "us-west-1"]
        cls.collector = EC2SAUCollector(
            regions=cls.regions,
            exclude_tags={"env": ["dev"]},
            client_getter=get_aws_client,
        )

    def test_log(self):
        self.assertEqual(self.log.level, "info")
        self.assertEqual(self.log.path, ".")
        self.assertEqual(self.log.retention, 7)

    def test_sau_collector(self):
        self.assertListEqual(list1=self.regions, list2=self.collector.regions)
        region = self.regions[0]
        response = self.collector.get_stopped_ec2(region=region)["response"]
        # test stopped ec2 logic
        self.assertListEqual(
            list1=[
                {
                    "name": "poc-sau01",
                    "region": "us-east-1",
                    "instanceid": "i-07fb37a99060c44",
                    "tag_environment": "development",
                    "tag_name": "poc-sau01",
                },
                {
                    "name": "poc-sau02",
                    "region": "us-east-1",
                    "instanceid": "i-07fb37a99060c44",
                    "tag_environment": "stage",
                    "tag_name": "poc-sau02",
                },
            ],
            list2=response,
        )
        response = self.collector.get_unattached_volumes(region=region)
        # test unattached volumes
        self.assertDictEqual(
            d1={
                "response": {
                    "states": {"unattached": 3, "error": 0},
                    "result": [
                        {
                            "name": "poc-sau-01",
                            "availabilityzone": "eu-central-1a",
                            "size": "20GB",
                            "volumeid": "vol-0c",
                            "volumetype": "gp3",
                            "state": "unattached",
                            "region": "us-east-1",
                            "tag_name": "poc-sau-01",
                            "tag_environment": "dev",
                        },
                        {
                            "name": "poc-sau-02",
                            "availabilityzone": "eu-central-1a",
                            "size": "20GB",
                            "volumeid": "vol-0d",
                            "volumetype": "gp3",
                            "state": "unattached",
                            "region": "us-east-1",
                            "tag_environment": "stage",
                            "tag_name": "poc-sau-02",
                        },
                        {
                            "name": "poc-sau-03",
                            "availabilityzone": "eu-central-1a",
                            "size": "15GB",
                            "volumeid": "vol-0ef",
                            "volumetype": "gp3",
                            "state": "unattached",
                            "region": "us-east-1",
                            "tag_environment": "stage",
                            "tag_name": "poc-sau-03",
                        },
                    ],
                },
                "errorcount": 0,
                "region": "us-east-1",
            },
            d2=response,
            msg="Unattached volumes dont match",
        )

        # test instance metrics
        response = self.collector.get_instance_metrics()
        self.assertDictEqual(
            d1={
                "stopped_instances": [
                    {
                        "name": "poc-sau01",
                        "region": "us-east-1",
                        "instanceid": "i-07fb37a99060c44",
                        "tag_environment": "development",
                        "tag_name": "poc-sau01",
                    },
                    {
                        "name": "poc-sau02",
                        "region": "us-east-1",
                        "instanceid": "i-07fb37a99060c44",
                        "tag_environment": "stage",
                        "tag_name": "poc-sau02",
                    },
                    {
                        "name": "poc-sau01",
                        "region": "us-west-1",
                        "instanceid": "i-07fb37a99060c44",
                        "tag_environment": "development",
                        "tag_name": "poc-sau01",
                    },
                    {
                        "name": "poc-sau02",
                        "region": "us-west-1",
                        "instanceid": "i-07fb37a99060c44",
                        "tag_environment": "stage",
                        "tag_name": "poc-sau02",
                    },
                ],
                "volumes": [
                    {
                        "name": "poc-sau-01",
                        "availabilityzone": "eu-central-1a",
                        "size": "20GB",
                        "volumeid": "vol-0c",
                        "volumetype": "gp3",
                        "state": "unattached",
                        "region": "us-east-1",
                        "tag_name": "poc-sau-01",
                        "tag_environment": "dev",
                    },
                    {
                        "name": "poc-sau-02",
                        "availabilityzone": "eu-central-1a",
                        "size": "20GB",
                        "volumeid": "vol-0d",
                        "volumetype": "gp3",
                        "state": "unattached",
                        "region": "us-east-1",
                        "tag_environment": "stage",
                        "tag_name": "poc-sau-02",
                    },
                    {
                        "name": "poc-sau-03",
                        "availabilityzone": "eu-central-1a",
                        "size": "15GB",
                        "volumeid": "vol-0ef",
                        "volumetype": "gp3",
                        "state": "unattached",
                        "region": "us-east-1",
                        "tag_environment": "stage",
                        "tag_name": "poc-sau-03",
                    },
                    {
                        "name": "poc-sau-01",
                        "availabilityzone": "eu-central-1a",
                        "size": "20GB",
                        "volumeid": "vol-0c",
                        "volumetype": "gp3",
                        "state": "unattached",
                        "region": "us-west-1",
                        "tag_name": "poc-sau-01",
                        "tag_environment": "dev",
                    },
                    {
                        "name": "poc-sau-02",
                        "availabilityzone": "eu-central-1a",
                        "size": "20GB",
                        "volumeid": "vol-0d",
                        "volumetype": "gp3",
                        "state": "unattached",
                        "region": "us-west-1",
                        "tag_environment": "stage",
                        "tag_name": "poc-sau-02",
                    },
                    {
                        "name": "poc-sau-03",
                        "availabilityzone": "eu-central-1a",
                        "size": "15GB",
                        "volumeid": "vol-0ef",
                        "volumetype": "gp3",
                        "state": "unattached",
                        "region": "us-west-1",
                        "tag_environment": "stage",
                        "tag_name": "poc-sau-03",
                    },
                ],
                "volume_states": {
                    "us-east-1": {"unattached": 3, "error": 0},
                    "us-west-1": {"unattached": 3, "error": 0},
                },
                "stopped_instances_count": {"us-east-1": 2, "us-west-1": 4},
            },
            d2=response,
        )

        # test doc
        self.assertNotEqual(first=self.collector.__doc__, second="")


    def test_is_excluded(self):
        test_args = [
            {"tags": {"inv_environment_id": "development"},
             "expected": False
            },
            {"tags": {"env": "dev"},
             "expected": True
            }
        ]
        for test_arg in test_args:
            response = self.collector.is_excluded(tags=test_arg["tags"])
            self.assertEqual(
                first=response,
                second=test_arg["expected"],
                msg=f"{test_arg}, response is not expected"
            )
            response = self.collector.is_not_excluded(tags=test_arg["tags"])
            self.assertEqual(
                first=response,
                second=not test_arg["expected"],
                msg=f"{test_arg}, response is not expected"
            )


    def test_util(self):
        self.assertEqual(first=self.util.default_exporter_port, second=9191)
        self.assertEqual(self.util.level, "info")
        self.assertEqual(self.util.path, ".")
        self.assertEqual(self.util.retention, 7)
        result = {
            "logging": {"retention": 7, "directory": ".", "level": "info", "handler": "both"},
            "exporter_port": 9191,
            "regions": ["eu-central-1", "eu-west-1"],
            "exclude_tags": {
                "inv_environment_id": ["development"],
                "inv_cluster_type": ["hansen"],
            },
        }
        filepath = os.path.dirname(os.path.abspath(__file__))
        config_file = f"{filepath}/../configs/config.yaml"
        self.assertDictEqual(d1=Util.read_yaml_file(filename=config_file), d2=result)
        self.assertDictEqual(d1=Util.get_config(filename=config_file), d2=result)
        self.assertIsInstance(obj=Util.version(), cls=str)

    def test_metrics_exposition_rejects_dotted_tag_label_names(self):
        """
        Reproduces https://github.com/NBCUDTC/nowtv-ansible/issues/9303:

        AWS tag keys containing '.' or '/' (e.g. the EBS CSI driver's
        `ebs.csi.aws.com/cluster` or Kubernetes' `kubernetes.io/created-for/pvc/name`)
        are turned into unquoted, non-ASCII Prometheus label names. That is
        invalid in the Prometheus text exposition format and causes
        Prometheus 3.x to fail the scrape with a hard parse error.

        With prometheus-client's default `underscores` escaping scheme
        (>=0.20), dotted/slashed tag keys are sanitised to `_` before being
        emitted, so this now passes.
        """
        collector = EC2SAUCollector(
            regions=["us-east-1"],
            exclude_tags={},
            client_getter=get_aws_client_with_dotted_tags,
        )
        registry = CollectorRegistry()
        registry.register(collector)
        exposition = generate_latest(registry).decode()

        # Sanity check: confirm our fixture's tag keys were sanitised
        # (dots/slashes -> underscores) rather than silently dropped.
        self.assertIn("tag_ebs_csi_aws_com_cluster=", exposition)
        self.assertIn(
            "tag_kubernetes_io_created_for_pvc_name=", exposition
        )

        legacy_label_name = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
        label_name_pattern = re.compile(r"[{,]([A-Za-z_][A-Za-z0-9_./]*)\s*=\s*\"")
        label_names = sorted(set(label_name_pattern.findall(exposition)))

        invalid_label_names = [
            name for name in label_names if not legacy_label_name.match(name)
        ]
        self.assertEqual(
            invalid_label_names,
            [],
            "exporter emitted Prometheus-invalid label name(s): "
            f"{invalid_label_names}. See "
            "https://github.com/NBCUDTC/nowtv-ansible/issues/9303",
        )

    def test_metrics_endpoint_ignores_accept_header_escaping(self):
        """
        Reproduces the "content negotiation does not help" part of
        https://github.com/NBCUDTC/nowtv-ansible/issues/9303: a client that
        requests `escaping=allow-utf-8` via the `Accept` header should
        receive quoted UTF-8 label names (and a `Content-Type` reflecting
        that escaping scheme), so it can scrape the raw tag-derived labels
        without them being invalid exposition.

        With prometheus-client's Accept-header content negotiation
        (>=0.20), the `/metrics` response now varies by escaping scheme:
        `escaping=allow-utf-8` yields quoted UTF-8 label names and a
        `Content-Type` reflecting that scheme.
        """
        collector = EC2SAUCollector(
            regions=["us-east-1"],
            exclude_tags={},
            client_getter=get_aws_client_with_dotted_tags,
        )
        registry = CollectorRegistry()
        registry.register(collector)
        app = make_wsgi_app(registry)

        def request(accept_header: str):
            captured = {}

            def start_response(status, headers):
                captured["status"] = status
                captured["headers"] = dict(headers)

            environ = {
                "REQUEST_METHOD": "GET",
                "PATH_INFO": "/metrics",
                "HTTP_ACCEPT": accept_header,
            }
            body = b"".join(app(environ, start_response))
            return body, captured["headers"]

        default_body, default_headers = request("*/*")
        utf8_body, utf8_headers = request(
            "application/openmetrics-text;version=1.0.0;charset=utf-8;escaping=allow-utf-8"
        )

        self.assertNotIn(
            "escaping=allow-utf-8",
            default_headers.get("Content-Type", ""),
            "default request should not negotiate UTF-8 escaping",
        )
        self.assertNotIn(b'"tag_ebs.csi.aws.com/cluster"=', default_body)
        self.assertIn(
            "escaping=allow-utf-8",
            utf8_headers.get("Content-Type", ""),
            "expected Content-Type to reflect the negotiated escaping=allow-utf-8 "
            f"scheme, got: {utf8_headers.get('Content-Type')!r}",
        )
        self.assertIn(
            b'"tag_ebs.csi.aws.com/cluster"=',
            utf8_body,
            "expected UTF-8 label names to be quoted when the client "
            "negotiates escaping=allow-utf-8",
        )


if __name__ == "__main__":
    unittest.main()
