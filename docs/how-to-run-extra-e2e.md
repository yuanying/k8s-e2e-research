# How to execute `extra e2e test`

## Requirement

-   python3
-   pip

## Install

```bash
$ pip install -r requirements.txt
```

### Apply patch

This extra e2e test run e2e test when one node in cluster is down.
But e2e test require all node is ready status.
You need patch to e2e code with below commands.

```bash
cd $GOPATH/src/k8s.io/kubernetes
patch --verbose -u -p1 --dry-run < e2e.patch # check for success
patch --verbose -u -p1 < e2e.patch
```

and compile e2e, see [Here](../README.md)

## Run test

```bash
$ export EE2E_TEST_CONFIG=${PATH_TO_CONFIG_FILE}
$ python -m unittest -v
```

### test config

Following yaml file is example of test config file.
Please change this to your own config.

```yaml
---
# Default username of virsh hosts
user: yuanying
# Default private key to ssh virsh hosts
private_key: ~/.ssh/id_rsa

kubernetes:
  kubectl_path: /usr/local/bin/kubectl
  context: test
  path: ~/go/src/k8s.io/kubernetes

ginkgo:
  focus: '(\[sig\-network\]\sDNS\sshould\sprovide\sDNS\sfor\sservices\s\[Conformance\])|(\[sig\-apps\]\sReplicaSet\sshould\sserve\sa\sbasic\simage\son\seach\sreplica\swith\sa\spublic\simage\s\[Conformance\])|(\[k8s\.io\]\sServiceAccounts\sshould\smount\san\sAPI\stoken\sinto\spods\s\[Conformance\])|(\[k8s\.io\]\sProjected\sshould\sbe\sconsumable\sfrom\spods\sin\svolume\s\[Conformance\]\s\[sig\-storage\])|(\[k8s\.io\]\sNetworking\s\[k8s\.io\]\sGranular\sChecks:\sPods\sshould\sfunction\sfor\sintra\-pod\scommunication)|(\[k8s\.io\]\sEmptyDir\svolumes\sshould\ssupport)'
  dryRun: 'true'

targets:
  '192.168.1.111':
    guestname: coreos-master01
    host: 192.168.200.4
  '192.168.1.112':
    guestname: coreos-master02
    host: 192.168.200.4
  '192.168.1.113':
    guestname: coreos-master03
    host: 192.168.200.5
  '192.168.1.121':
    guestname: coreos-worker01
    host: 192.168.200.4
  '192.168.1.122':
    guestname: coreos-worker02
    host: 192.168.200.5
  '192.168.1.123':
    guestname: coreos-worker03
    host: 192.168.200.4

virsh_hosts:
  '192.168.200.4': {}
  '192.168.200.5': {}

```
