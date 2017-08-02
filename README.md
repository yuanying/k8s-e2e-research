# k8s-e2e-research

## Install Go 1.8.3

```bash
export GOPATH=~/go
echo "export GOPATH=~/go" >> ~/.bashrc
export PATH=$PATH:/usr/local/go/bin
echo "export PATH=$PATH:/usr/local/go/bin"  >> ~/.bashrc
export KUBECTL_PATH=/usr/local/bin/kubectl
echo "export KUBECTL_PATH=/usr/local/bin/kubectl"  >> ~/.bashrc
curl -O https://storage.googleapis.com/golang/go1.8.3.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.8.3.linux-amd64.tar.gz
```

## Install Kubernetes

```bash
$ go get k8s.io/kubernetes
```

## Install kubectl

```bash
$ curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
$ chmod +x kubectl
$ sudo mv kubectl /usr/local/bin/
```

## Compile required binaries

See: https://github.com/kubernetes/kubernetes/blob/release-1.7/build/root/Makefile#L197

```bash
$ sudo usermod -a -G docker ${USER} # Need re-login
$ cd $GOPATH/src/k8s.io/kubernetes
$ make quick-release
$ make ginkgo
$ make generated_files
```

## Conformance Test

> [Conformance] tests represent a subset of the e2e-tests
> we expect to pass on any Kubernetes cluster.

```bash
$ export KUBECONFIG=/path/to/kubeconfig
$ export KUBERNETES_CONFORMANCE_TEST=true
$ export KUBERNETES_PROVIDER=skeleton
```

自分で建てた Kubernetes Cluster に対して e2e テストをするのに使える。

## JUnit 形式の結果ファイル

`E2E_REPORT_DIR` を指定することで、そこに JUnit 形式の結果ファイルが出力される。

```bash
$ export E2E_REPORT_DIR=/path/to/e2e-result-xml
```

## Dry Run

とりあえずどんなテストが走るのか試してみる。

```bash
$ go run hack/e2e.go -- -v --test --test_args="--ginkgo.dryRun=true"
$ go run hack/e2e.go -- -v --test --test_args="--ginkgo.dryRun=true --ginkgo.focus=\[Conformance\]"
```

`--ginkgo.focus=\[Conformance\]` することで Conformance テストだけ流すことが可能。

## Run

Slow タグがついてるテストだけ除外とかもできる。

```bash
$ go run hack/e2e.go -- -v --test --test_args="--ginkgo.focus=\[Conformance\]"
$ go run hack/e2e.go -- -v --test --test_args="--ginkgo.dryRun=true --ginkgo.focus=\[Conformance\] --ginkgo.skip=\[Slow\]"
$ go run hack/e2e.go -- -v --test --test_args="--ginkgo.focus=\[sig-cli\].*\[Conformance\] --ginkgo.skip=\[Slow\]" # Conformance テストの中でも sig-cli タグがついたもののみテスト。
```

## 結果の一覧

### 名前でソート

```bash
$ ruby ./summary.rb category
[sig-scheduling] SchedulerPredicates [Serial] validates that NodeSelector is respected if not matching [Conformance] (86.921161049s)
[sig-scheduling] SchedulerPredicates [Serial] validates that NodeSelector is respected if matching [Conformance] (93.522141976s)
[sig-scheduling] SchedulerPredicates [Serial] validates resource limits of pods that are allowed to run [Conformance] (140.845898374s)
[sig-network] Services should serve multiport endpoints from pods [Conformance] (35.577782706s)
[sig-network] Services should serve a basic endpoint from pods [Conformance] (17.730461556s)
[sig-network] Services should provide secure master service [Conformance] (6.45621956s)
[sig-network] Networking should provide Internet connection for containers [Conformance] (13.203357804s)
[sig-network] DNS should provide DNS for the cluster [Conformance] (23.164413487s)
[sig-network] DNS should provide DNS for services [Conformance] (26.144564992s)
[sig-cli] Kubectl client [k8s.io] Update Demo should scale a replication controller [Conformance] (46.21784705s)
[sig-cli] Kubectl client [k8s.io] Update Demo should do a rolling update of a replication controller [Conformance] (47.271536654s)
[sig-cli] Kubectl client [k8s.io] Update Demo should create and stop a replication controller [Conformance] (16.949727919s)
[sig-cli] Kubectl client [k8s.io] Proxy server should support proxy with --port 0 [Conformance] (6.6695880800000005s)
[sig-cli] Kubectl client [k8s.io] Proxy server should support --unix-socket=/path [Conformance] (6.600578366s)
[sig-cli] Kubectl client [k8s.io] Kubectl version should check is all data is printed [Conformance] (6.707831641s)
[sig-cli] Kubectl client [k8s.io] Kubectl run rc should create an rc from an image [Conformance] (30.214375242s)
[sig-cli] Kubectl client [k8s.io] Kubectl run pod should create a pod from an image when restart is Never [Conformance] (7.305298506s)
[sig-cli] Kubectl client [k8s.io] Kubectl run job should create a job from an image when restart is OnFailure [Conformance] (11.447821062s)
[sig-cli] Kubectl client [k8s.io] Kubectl run deployment should create a deployment from an image [Conformance] (16.689211853s)
[sig-cli] Kubectl client [k8s.io] Kubectl run default should create an rc or deployment from an image [Conformance] (92.537657562s)
[sig-cli] Kubectl client [k8s.io] Kubectl run --rm job should create a job from an image, then delete the job [Conformance] (14.707360616s)
[sig-cli] Kubectl client [k8s.io] Kubectl rolling-update should support rolling-update to same image [Conformance] (25.46421606s)
[sig-cli] Kubectl client [k8s.io] Kubectl replace should update a single-container pod&#39;s image [Conformance] (12.891327778s)
[sig-cli] Kubectl client [k8s.io] Kubectl patch should add annotations for pods in rc [Conformance] (29.750334355s)
[sig-cli] Kubectl client [k8s.io] Kubectl logs should be able to retrieve and filter logs [Conformance] (33.212352061s)
[sig-cli] Kubectl client [k8s.io] Kubectl label should update the label on a resource [Conformance] (14.909215776s)
[sig-cli] Kubectl client [k8s.io] Kubectl expose should create services for rc [Conformance] (33.518730378s)
[sig-cli] Kubectl client [k8s.io] Kubectl describe should check if kubectl describe prints relevant information for rc and pods [Conformance] (29.601465592s)
[sig-cli] Kubectl client [k8s.io] Kubectl cluster-info should check if Kubernetes master services is included in cluster-info [Conformance] (6.749272876s)
[sig-cli] Kubectl client [k8s.io] Kubectl api-versions should check if v1 is in available api versions [Conformance] (6.7865929640000004s)
[sig-cli] Kubectl client [k8s.io] Guestbook application should create and stop a working application [Conformance] (85.659561321s)
[sig-cli] Kubectl Proxy version v1 should proxy through a service and a pod [Conformance] (24.332731053s)
[sig-cli] Kubectl Proxy version v1 should proxy logs on node with explicit kubelet port using proxy subresource [Conformance] (6.788559451s)
[sig-cli] Kubectl Proxy version v1 should proxy logs on node with explicit kubelet port [Conformance] (6.937862467s)
[sig-cli] Kubectl Proxy version v1 should proxy logs on node using proxy subresource [Conformance] (6.510252329s)
[sig-cli] Kubectl Proxy version v1 should proxy logs on node [Conformance] (6.5902387749999995s)
[sig-apps] ReplicationController should serve a basic image on each replica with a public image [Conformance] (18.534921923s)
[sig-apps] ReplicaSet should serve a basic image on each replica with a public image [Conformance] (18.818012545s)
[sig-api-machinery] CustomResourceDefinition resources Simple CustomResourceDefinition creating/deleting custom resource definition objects works [Conformance] (10.53801226s)
[k8s.io] Variable Expansion should allow substituting values in a container&#39;s command [Conformance] (12.917167114s)
[k8s.io] Variable Expansion should allow substituting values in a container&#39;s args [Conformance] (10.970171491s)
[k8s.io] Variable Expansion should allow composing env vars into new env vars [Conformance] (13.252649142s)
[k8s.io] ServiceAccounts should mount an API token into pods [Conformance] (26.416414296s)
[k8s.io] ServiceAccounts should allow opting out of API token automount [Conformance] (35.121860302s)
[k8s.io] Service endpoints latency should not be very high [Conformance] (94.304421907s)
[k8s.io] Secrets should be consumable via the environment [Conformance] (11.274664851s)
[k8s.io] Secrets should be consumable in multiple volumes in a pod [Conformance] [sig-storage] (12.773822256s)
[k8s.io] Secrets should be consumable from pods in volume with mappings and Item Mode set [Conformance] [sig-storage] (8.719920178s)
[k8s.io] Secrets should be consumable from pods in volume with mappings [Conformance] [sig-storage] (10.86726149s)
[k8s.io] Secrets should be consumable from pods in volume with defaultMode set [Conformance] [sig-storage] (11.256213673s)
[k8s.io] Secrets should be consumable from pods in volume as non-root with defaultMode and fsGroup set [Conformance] [sig-storage] (12.798172597s)
[k8s.io] Secrets should be consumable from pods in volume [Conformance] [sig-storage] (11.129206919s)
[k8s.io] Secrets should be consumable from pods in env vars [Conformance] (11.264523719s)
[k8s.io] Secrets optional updates should be reflected in volume [Conformance] [sig-storage] (121.949083013s)
[k8s.io] Projected updates should be reflected in volume [Conformance] [sig-storage] (105.809851035s)
[k8s.io] Projected should update labels on modification [Conformance] [sig-storage] (31.31347541s)
[k8s.io] Projected should update annotations on modification [Conformance] [sig-storage] (118.130021762s)
[k8s.io] Projected should set mode on item file [Conformance] [sig-storage] (13.693248183s)
[k8s.io] Projected should set DefaultMode on files [Conformance] [sig-storage] (10.767802074s)
[k8s.io] Projected should provide podname only [Conformance] [sig-storage] (11.23987248s)
[k8s.io] Projected should provide node allocatable (memory) as default memory limit if the limit is not set [Conformance] [sig-storage] (10.830098552s)
[k8s.io] Projected should provide node allocatable (cpu) as default cpu limit if the limit is not set [Conformance] [sig-storage] (10.789174651s)
[k8s.io] Projected should provide container&#39;s memory request [Conformance] [sig-storage] (10.701792756s)
[k8s.io] Projected should provide container&#39;s memory limit [Conformance] [sig-storage] (10.884277082s)
[k8s.io] Projected should provide container&#39;s cpu request [Conformance] [sig-storage] (10.549702226s)
[k8s.io] Projected should provide container&#39;s cpu limit [Conformance] [sig-storage] (11.004414274s)
[k8s.io] Projected should project all components that make up the projection API [Conformance] [sig-storage] [Projection] (10.694738139s)
[k8s.io] Projected should be consumable in multiple volumes in the same pod [Conformance] [sig-storage] (10.896274756s)
[k8s.io] Projected should be consumable in multiple volumes in a pod [Conformance] [sig-storage] (10.915899341s)
[k8s.io] Projected should be consumable from pods in volume with mappings as non-root [Conformance] [sig-storage] (13.333880069s)
[k8s.io] Projected should be consumable from pods in volume with mappings and Item mode set[Conformance] [sig-storage] (10.93681715s)
[k8s.io] Projected should be consumable from pods in volume with mappings and Item Mode set [Conformance] [sig-storage] (11.36272339s)
[k8s.io] Projected should be consumable from pods in volume with mappings [Conformance] [sig-storage] (10.864511563s)
[k8s.io] Projected should be consumable from pods in volume with mappings [Conformance] [sig-storage] (10.774236199s)
[k8s.io] Projected should be consumable from pods in volume with defaultMode set [Conformance] [sig-storage] (11.02158347s)
[k8s.io] Projected should be consumable from pods in volume with defaultMode set [Conformance] [sig-storage] (8.892022698s)
[k8s.io] Projected should be consumable from pods in volume as non-root with defaultMode and fsGroup set [Conformance] [sig-storage] (10.819535627s)
[k8s.io] Projected should be consumable from pods in volume as non-root [Conformance] [sig-storage] (11.223900183s)
[k8s.io] Projected should be consumable from pods in volume [Conformance] [sig-storage] (10.569457576s)
[k8s.io] Projected should be consumable from pods in volume [Conformance] [sig-storage] (11.035480444s)
[k8s.io] Projected optional updates should be reflected in volume [Conformance] [sig-storage] (111.87457874s)
[k8s.io] Projected optional updates should be reflected in volume [Conformance] [sig-storage] (35.254768815s)
[k8s.io] Probing container with readiness probe that fails should never be ready and never restart [Conformance] (84.664430608s)
[k8s.io] Probing container with readiness probe should not be ready before initial delay and never restart [Conformance] (46.527781972s)
[k8s.io] Probing container should be restarted with a exec &#34;cat /tmp/health&#34; liveness probe [Conformance] (60.983078919s)
[k8s.io] Probing container should be restarted with a docker exec liveness probe with timeout [Conformance] (6.629339677s)
[k8s.io] Probing container should be restarted with a /healthz http liveness probe [Conformance] (29.028056526s)
[k8s.io] Probing container should *not* be restarted with a exec &#34;cat /tmp/health&#34; liveness probe [Conformance] (131.421568273s)
[k8s.io] Probing container should *not* be restarted with a /healthz http liveness probe [Conformance] (134.914177027s)
[k8s.io] PreStop should call prestop when killing a pod [Conformance] (53.71507659s)
[k8s.io] Pods should get a host IP [Conformance] (28.745763066s)
[k8s.io] Pods should contain environment variables for services [Conformance] (31.370916034s)
[k8s.io] Pods should be updated [Conformance] (27.487256573s)
[k8s.io] Pods should be submitted and removed [Conformance] (20.519077989s)
[k8s.io] Pods should allow activeDeadlineSeconds to be updated [Conformance] (15.459555856s)
[k8s.io] Pods Extended [k8s.io] Pods Set QOS Class should be submitted and removed [Conformance] (25.070818828s)
[k8s.io] Pods Extended [k8s.io] Delete Grace Period should be submitted and removed [Conformance] [Flaky] (15.801193457s)
[k8s.io] Networking [k8s.io] Granular Checks: Pods should function for node-pod communication: udp [Conformance] (71.422288079s)
[k8s.io] Networking [k8s.io] Granular Checks: Pods should function for node-pod communication: http [Conformance] (51.357676902s)
[k8s.io] Networking [k8s.io] Granular Checks: Pods should function for intra-pod communication: udp [Conformance] (62.42842178s)
[k8s.io] Networking [k8s.io] Granular Checks: Pods should function for intra-pod communication: http [Conformance] (64.524437329s)
[k8s.io] KubeletManagedEtcHosts should test kubelet managed /etc/hosts file [Conformance] (61.258978268s)
[k8s.io] HostPath should give a volume the correct mode [Conformance] [sig-storage] (13.082017435s)
[k8s.io] Events should be sent by kubelets and the scheduler about pods scheduling and running [Conformance] (15.088337998s)
[k8s.io] EmptyDir volumes volume on tmpfs should have the correct mode [Conformance] [sig-storage] (10.651851858s)
[k8s.io] EmptyDir volumes volume on default medium should have the correct mode [Conformance] [sig-storage] (12.725269911s)
[k8s.io] EmptyDir volumes should support (root,0777,tmpfs) [Conformance] [sig-storage] (10.645797215s)
[k8s.io] EmptyDir volumes should support (root,0777,default) [Conformance] [sig-storage] (12.788574576s)
[k8s.io] EmptyDir volumes should support (root,0666,tmpfs) [Conformance] [sig-storage] (13.517565241s)
[k8s.io] EmptyDir volumes should support (root,0666,default) [Conformance] [sig-storage] (13.340508866s)
[k8s.io] EmptyDir volumes should support (root,0644,tmpfs) [Conformance] [sig-storage] (9.086963342s)
[k8s.io] EmptyDir volumes should support (root,0644,default) [Conformance] [sig-storage] (10.950929654s)
[k8s.io] EmptyDir volumes should support (non-root,0777,tmpfs) [Conformance] [sig-storage] (11.374834994s)
[k8s.io] EmptyDir volumes should support (non-root,0777,default) [Conformance] [sig-storage] (10.829619138s)
[k8s.io] EmptyDir volumes should support (non-root,0666,tmpfs) [Conformance] [sig-storage] (10.68826638s)
[k8s.io] EmptyDir volumes should support (non-root,0666,default) [Conformance] [sig-storage] (13.35167412s)
[k8s.io] EmptyDir volumes should support (non-root,0644,tmpfs) [Conformance] [sig-storage] (13.18148715s)
[k8s.io] EmptyDir volumes should support (non-root,0644,default) [Conformance] [sig-storage] (10.67365538s)
[k8s.io] Downward API volume should update labels on modification [Conformance] [sig-storage] (94.175059146s)
[k8s.io] Downward API volume should update annotations on modification [Conformance] [sig-storage] (108.536100554s)
[k8s.io] Downward API volume should set mode on item file [Conformance] [sig-storage] (11.015293398s)
[k8s.io] Downward API volume should set DefaultMode on files [Conformance] [sig-storage] (10.827933823s)
[k8s.io] Downward API volume should provide podname only [Conformance] [sig-storage] (10.79249949s)
[k8s.io] Downward API volume should provide node allocatable (memory) as default memory limit if the limit is not set [Conformance] [sig-storage] (13.099323733s)
[k8s.io] Downward API volume should provide node allocatable (cpu) as default cpu limit if the limit is not set [Conformance] [sig-storage] (11.666057803s)
[k8s.io] Downward API volume should provide container&#39;s memory request [Conformance] [sig-storage] (10.930260648s)
[k8s.io] Downward API volume should provide container&#39;s memory limit [Conformance] [sig-storage] (10.770234304s)
[k8s.io] Downward API volume should provide container&#39;s cpu request [Conformance] [sig-storage] (11.526263569s)
[k8s.io] Downward API volume should provide container&#39;s cpu limit [Conformance] [sig-storage] (12.610064429s)
[k8s.io] Downward API should provide pod name and namespace as env vars [Conformance] (10.666264608s)
[k8s.io] Downward API should provide pod and host IP as an env var [Conformance] (13.028049816s)
[k8s.io] Downward API should provide default limits.cpu/memory from node allocatable [Conformance] (10.612601358s)
[k8s.io] Downward API should provide container&#39;s limits.cpu/memory and requests.cpu/memory as env vars [Conformance] (10.804534396s)
[k8s.io] Docker Containers should use the image defaults if command and args are blank [Conformance] (10.883642668s)
[k8s.io] Docker Containers should be able to override the image&#39;s default commmand (docker entrypoint) [Conformance] (10.680783518s)
[k8s.io] Docker Containers should be able to override the image&#39;s default command and arguments [Conformance] (11.292484658s)
[k8s.io] Docker Containers should be able to override the image&#39;s default arguments (docker cmd) [Conformance] (10.628335346s)
[k8s.io] ConfigMap updates should be reflected in volume [Conformance] [sig-storage] (116.350034072s)
[k8s.io] ConfigMap should be consumable via the environment [Conformance] (13.290114321s)
[k8s.io] ConfigMap should be consumable via environment variable [Conformance] (12.951395776s)
[k8s.io] ConfigMap should be consumable in multiple volumes in the same pod [Conformance] [sig-storage] (12.880226564s)
[k8s.io] ConfigMap should be consumable from pods in volume with mappings as non-root [Conformance] [sig-storage] (10.737706653s)
[k8s.io] ConfigMap should be consumable from pods in volume with mappings and Item mode set[Conformance] [sig-storage] (13.391051976s)
[k8s.io] ConfigMap should be consumable from pods in volume with mappings [Conformance] [sig-storage] (11.404350151s)
[k8s.io] ConfigMap should be consumable from pods in volume with defaultMode set [Conformance] [sig-storage] (14.58943899s)
[k8s.io] ConfigMap should be consumable from pods in volume as non-root [Conformance] [sig-storage] (13.056127381s)
[k8s.io] ConfigMap should be consumable from pods in volume [Conformance] [sig-storage] (10.798915554s)
[k8s.io] ConfigMap optional updates should be reflected in volume [Conformance] [sig-storage] (114.406202769s)
```

### 実行時間でソート

```bash
$ ruby ./summary.rb time
```
