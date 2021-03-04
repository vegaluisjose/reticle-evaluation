set verilog_file [lindex $argv 0]
set constraint_file [lindex $argv 1]
set timing_file [lindex $argv 2]
set util_file [lindex $argv 3]

set part_name "xczu3eg-sbva484-1-e"

read_verilog -sv $verilog_file
read_xdc -mode out_of_context $constraint_file
synth_design -mode "out_of_context" -flatten_hierarchy "rebuilt" -top "main" -part $part_name
place_design -directive Default
route_design -directive Default
report_timing -file $timing_file
report_utilization -file $util_file
