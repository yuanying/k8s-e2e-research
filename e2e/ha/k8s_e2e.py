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
import re
import subprocess
import time

import paramiko

from e2e import base


class HATestBase(base.TestCase):

    env = {}
    connections = {}
    target = None

    @classmethod
    def setUpClass(cls):
        subprocess.check_call("{} config set-context {}".format(
            cls.kubectl_path(),
            cls.kubectl_context(),
        ), shell=True)
        for virsh_host, params in cls.env.get('virsh_hosts', {}).items():
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            pkey = paramiko.RSAKey.from_private_key_file(
                cls.get_private_key_path(virsh_host)
            )
            username = cls.get_virsh_hosts_value(virsh_host, 'user')
            c.connect(virsh_host, username=username, pkey=pkey)

            cls.connections[virsh_host] = c

    @classmethod
    def kubectl_path(cls):
        return cls.env['kubernetes']['kubectl_path']

    @classmethod
    def kubectl_context(cls):
        return cls.env['kubernetes']['context']

    @classmethod
    def get_private_key_path(cls, target):
        return os.path.expanduser(
            cls.get_virsh_hosts_value(target, 'private_key')
        )


    @classmethod
    def get_virsh_hosts_value(cls, target, key):
        v = cls.env.get('virsh_hosts', {}).get(target, {}).get(key, None)
        if not v:
            v = cls.env.get(key, None)

        return v

    @classmethod
    def tearDownClass(cls):
        for c in cls.connections.values():
            c.close()

    def setUp(self):
        client = self.ssh_host_conn()
        command = 'sudo virsh destroy {}'.format(self.guestname())
        client.exec_command(command)

        self.check_subprocess_output(
            "kubectl get nodes {}".format(self.target),
            'NotReady'
        )

    def tearDown(self):
        client = self.ssh_host_conn()
        command = 'sudo virsh start {}'.format(self.guestname())
        client.exec_command(command)

        while True:
            _, stdout, _ = client.exec_command(
                'sudo virsh domstate {}'.format(self.guestname())
            )
            domstate = stdout.read().strip()
            print(domstate)
            if domstate == b'running':
                break

            time.sleep(3)

        self.check_subprocess_output(
            "kubectl get nodes {}".format(self.target),
            'Ready'
        )

    def test_health(self):
        self.assertEqual(True, True)
        output = subprocess.check_output(
            "kubectl get nodes {}".format(self.target),
            shell=True
        ).decode("utf-8")
        self.assertRegex(output, 'Ready')

    def guestname(self):
        return self.target_info()['guestname']

    def host(self):
        return self.target_info()['host']

    def target_info(self):
        return self.env['targets'][self.target]

    def ssh_host_conn(self):
        return self.connections[self.host()]

    def check_subprocess_output(cmd, pass_string, attempts=3):
        while True:
            try:
                output = subprocess.check_output(
                    cmd,
                    shell=True
                ).decode('utf-8')
                print(output)
                if re.search(pass_string, output):
                    break
            except Exception as e:
                attempts = attempts - 1
                if attempts < 0:
                    raise
