#!/usr/bin/env ruby -wKU

tests = [
  '[sig-network] DNS should provide DNS for services [Conformance]',
  '[sig-apps] ReplicaSet should serve a basic image on each replica with a public image [Conformance]',
  '[k8s.io] ServiceAccounts should mount an API token into pods [Conformance]',
  '[k8s.io] Projected should be consumable from pods in volume [Conformance] [sig-storage]',
  '[k8s.io] Networking [k8s.io] Granular Checks: Pods should function for intra-pod communication',
  '[k8s.io] EmptyDir volumes should support',
]

tests.map! do |e|
  e = "(#{Regexp.escape(e)})"
  e.gsub!(/\\\s/, '\s')
end

tests = tests.join('|')

puts "-----------------------------Dry Run-----------------------------"
puts "go run hack/e2e.go -- -v --test --test_args=\"--ginkgo.dryRun=true --ginkgo.focus=#{tests}\""
puts "----------------------------Actual Run---------------------------"
puts "go run hack/e2e.go -- -v --test --test_args=\"--ginkgo.focus=#{tests}\""
