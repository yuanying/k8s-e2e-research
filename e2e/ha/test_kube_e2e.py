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

import sys
import unittest

from e2e import base
from e2e.ha import k8s_e2e


def define_tests():
    for target, params in base.config['targets'].items():
        k8s_e2e.HATestBase.env = base.config
        clazz = type(
            "HATest${}".format(target),
            (k8s_e2e.HATestBase,),
            { "target": target }
        )
        setattr(sys.modules[__name__], "HATest%s" % target, clazz)


define_tests()
