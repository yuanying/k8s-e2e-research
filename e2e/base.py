#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import yaml
import unittest


__cur_dir = os.path.abspath(os.path.dirname(__file__))
__default_config = os.path.join(__cur_dir, 'configs', 'elk.yaml')
config = os.getenv("EE2E_TEST_CONFIG", __default_config)
config = yaml.safe_load(open(config).read())


class TestCase(unittest.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
