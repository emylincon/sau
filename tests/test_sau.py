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
import unittest

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, f"{os.path.dirname(os.path.abspath(__file__))}/../src/")

from sau.__main__ import Log, Util, EC2SAUCollector


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = Log()
        cls.util = Util()
        cls.regions = ["us-east-1", "us-west-1"]
        cls.collector = EC2SAUCollector(regions=cls.regions)

    def test_log(self):
        self.assertEqual(self.log.level, "info")
        self.assertEqual(self.log.path, ".")
        self.assertEqual(self.log.retention, 7)

    def test_sau_collector(self):
        self.assertListEqual(list1=self.regions, list2=self.collector.regions)
        region = self.regions[0]
        self.assertListEqual(
            list1=[],
            list2=self.collector.get_stopped_ec2(region=region)["response"],
        )
        d1 = {
            "response": {"states": {"unattached": 0, "error": 0}, "result": []},
            "errorcount": 1,
            "region": region,
        }
        self.assertDictEqual(
            d1=d1, d2=self.collector.get_unattached_volumes(region=region)
        )
        d1 = {
            "stopped_instances": [],
            "volumes": [],
            "volume_states": {
                region: {"unattached": 0, "error": 0} for region in self.regions
            },
            "stopped_instances_count": {region: 0 for region in self.regions},
        }
        self.assertDictEqual(d1=d1, d2=self.collector.get_instance_metrics())
        self.assertNotEqual(first=self.collector.__doc__, second="")

    def test_util(self):
        self.assertEqual(first=self.util.default_exporter_port, second=9191)
        self.assertEqual(self.util.level, "info")
        self.assertEqual(self.util.path, ".")
        self.assertEqual(self.util.retention, 7)
        result = {
            "logging": {"retention": 7, "directory": ".", "level": "info"},
            "exporter_port": 9191,
            "regions": ["eu-central-1", "eu-west-1"],
        }
        filepath = os.path.dirname(os.path.abspath(__file__))
        config_file = f"{filepath}/../configs/config.yaml"
        self.assertDictEqual(d1=Util.read_yaml_file(filename=config_file), d2=result)
        self.assertDictEqual(d1=Util.get_config(filename=config_file), d2=result)
        self.assertIsInstance(obj=Util.version(), cls=str)


if __name__ == "__main__":
    unittest.main()
