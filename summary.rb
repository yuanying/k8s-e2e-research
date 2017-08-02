#!/usr/bin/env ruby -wKU

results = []

mode = ARGV[0] || 'time'
result_path = File.join(File.dirname(__FILE__), 'junit_01.xml')

open(result_path) do |io|
  io.each_line do |line|
    if /<testcase name="(.+?)".* time="(\d+\.\d+)".*/ =~ line
      results << [$2, $1]
    end
  end
end

if mode == 'time'
  results = results.sort {|a, b| b[0].to_i <=> a[0].to_i }
else
  results = results.sort {|a, b| b[1] <=> a[1] }
end

results.each do |line|
  puts "-   #{line[1]} (#{line[0]}s)"
end
