set verilog_file [lindex $argv 0]

set part_name "xczu3eg-sbva484-1-e"

read_verilog -sv $verilog_file
synth_design -mode "out_of_context" -flatten_hierarchy "rebuilt" -top "main" -part $part_name
opt_design
place_design -directive Default
