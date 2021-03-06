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

        cls.shutdown_node()

    @classmethod
    def tearDownClass(cls):
        cls.start_node()
        for c in cls.connections.values():
            c.close()

    @classmethod
    def kubectl_path(cls):
        return cls.kube_param('kubectl_path')

    @classmethod
    def kubectl_context(cls):
        return cls.kube_param('context')

    @classmethod
    def k8s_path(cls):
        return os.path.expanduser(
            cls.kube_param('path')
        )

    @classmethod
    def kube_param(cls, key):
        return cls.env['kubernetes'].get(key, None)

    @classmethod
    def ginkgo_param(cls, key):
        return cls.env['ginkgo'].get(key, None)

    @classmethod
    def ginkgo_focus(cls):
        return cls.ginkgo_param('focus')

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
    def shutdown_node(cls):
        client = cls.ssh_host_conn()
        command = 'sudo virsh destroy {}'.format(cls.guestname())
        client.exec_command(command)

        cls.check_subprocess_output(
            "{} get nodes {}".format(
                cls.kubectl_path(),
                cls.target,
            ),
            'NotReady'
        )

    @classmethod
    def start_node(cls):
        client = cls.ssh_host_conn()
        command = 'sudo virsh start {}'.format(cls.guestname())
        client.exec_command(command)

        while True:
            _, stdout, _ = client.exec_command(
                'sudo virsh domstate {}'.format(cls.guestname())
            )
            domstate = stdout.read().strip()
            print(domstate)
            if domstate == b'running':
                break

            time.sleep(3)

        cls.check_subprocess_output(
            "{} get nodes {}".format(
                cls.kubectl_path(),
                cls.target,
            ),
            ' Ready'
        )

    @classmethod
    def guestname(self):
        return self.target_info()['guestname']

    @classmethod
    def host(self):
        return self.target_info()['host']

    @classmethod
    def target_info(self):
        return self.env['targets'][self.target]

    @classmethod
    def ssh_host_conn(self):
        return self.connections[self.host()]

    @classmethod
    def check_subprocess_output(self, cmd, pass_string, attempts=3):
        while True:
            try:
                output = subprocess.check_output(
                    cmd,
                    shell=True
                ).decode('utf-8')
                print(output)
                time.sleep(3)
                if re.search(pass_string, output):
                    break
            except Exception as e:
                attempts = attempts - 1
                if attempts < 0:
                    raise

    def test_health(self):
        self.assertEqual(True, True)
        output = subprocess.check_output(
            "{} get nodes {}".format(self.kubectl_path(), self.target),
            shell=True
        ).decode("utf-8")
        self.assertRegex(output, 'NotReady')

    def test_e2e(self):
        myenv = os.environ.copy()
        myenv['KUBERNETES_CONFORMANCE_TEST'] = 'true'
        myenv['KUBERNETES_PROVIDER'] = 'skelton'
        cmd = (
            'go run hack/e2e.go '
            '-- -v --test '
            '--test_args="--ginkgo.dryRun={dryRun} --ginkgo.focus={focus}"'
        ).format(
            dryRun=self.ginkgo_param('dryRun'),
            focus=self.ginkgo_focus(),
        )
        cwd = self.k8s_path()

        output = subprocess.check_output(
            cmd, shell=True, cwd=cwd, env=myenv
        ).decode('utf-8')
        print(output)
