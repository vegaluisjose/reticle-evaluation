import os
from utilities import *
import pandas as pd
import re


def build_util_pattern(start, end):
    return r".*{}\s+\|\s+(\b\d+\b)\s+\|\s+{}.*".format(start, end)


def build_util_pattern_map():
    pat = {}
    for i in range(1, 7):
        pat["lut{}".format(i)] = build_util_pattern("LUT{}".format(i), "CLB")
    pat["dsp"] = build_util_pattern("DSP48E2", "Arithmetic")
    comp = {}
    for k, v in pat.items():
        comp[k] = re.compile(v)
    return comp


def build_runtime_pattern():
    return re.compile(r"Data Path Delay:\s+(\d+\.\d+).*")


def count(data, types):
    num = 0
    for t in types:
        if t in data:
            num += data[t]
    return num


def parse_util(data, path, length, backend):
    input = {}
    with open(path, "r") as file:
        for f in file:
            for k, pat in build_util_pattern_map().items():
                m = re.search(pat, f)
                if m is not None:
                    input[k] = int(m.group(1))
    num = {}
    num["lut"] = count(input, ["lut{}".format(i) for i in range(1, 7)])
    num["dsp"] = count(input, ["dsp"])
    for k, v in num.items():
        data = update_util(data, backend, length, v, k)
    return data


def parse_time(data, path, length, backend):
    pat = build_runtime_pattern()
    with open(path, "r") as file:
        for f in file:
            m = re.search(pat, f)
            if m is not None:
                runtime = float(m.group(1))
                data = update_time(data, backend, length, runtime)
    return data


def run(prog):
    backends = ["base", "hint", "reticle"]
    progs = get_prog_list(prog)
    lens = get_prog_len(prog)
    data_time = {}
    data_util = {}
    constraints = get_constraint_path()
    for b in backends:
        make_source_dir(b)
        make_result_dir(b)
        for p, l in zip(progs, lens):
            inp = get_inp_prog_path(p)
            out = get_out_prog_path(b, p)
            time = get_out_timing_path(b, p)
            util = get_out_util_path(b, p)
            print("Compiling {} with [{}] backend...".format(inp, b))
            if b == "base":
                compile_ir_to_base(inp, out)
                compile_vivado("baseline", [out, constraints, time, util])
            elif b == "hint":
                compile_ir_to_hint(inp, out)
                compile_vivado("baseline", [out, constraints, time, util])
            elif b == "reticle":
                compile_ir_to_struct_placed(inp, out)
                compile_vivado("reticle", [out, constraints, time, util])
            data_time = parse_time(data_time, time, l, b)
            data_util = parse_util(data_util, util, l, b)
    df_time = pd.DataFrame.from_dict(data_time)
    df_util = pd.DataFrame.from_dict(data_util)
    csv_name = "{}.csv".format(prog)
    time_path = os.path.join(
        get_scripts_dir(), "..", "data", "runtime", csv_name
    )
    util_path = os.path.join(get_scripts_dir(), "..", "data", "util", csv_name)
    df_time.to_csv(time_path, index=False)
    df_util.to_csv(util_path, index=False)


if __name__ == "__main__":
    progs = ["tadd", "tdot", "fsm"]
    for p in progs:
        run(p)
    cleanup_vivado_files()
