import os
from utilities import *
import pandas as pd


def get_prog_len_debug(prog):
    if prog == "tadd":
        return [64]
    elif prog == "tdot":
        return [0]
    elif prog == "fsm":
        return [3]
    else:
        return []


def get_prog_list_debug(prog):
    if prog == "tadd":
        return ["tadd_64"]
    elif prog == "tdot":
        return ["tdot_5_3"]
    elif prog == "fsm":
        return ["fsm_3"]
    else:
        return []


def run(prog):
    backends = ["base", "hint", "reticle"]
    progs = get_prog_list_debug(prog)
    lens = get_prog_len_debug(prog)
    data = {}
    for b in backends:
        make_source_dir(b)
        make_result_dir(b)
        for p, l in zip(progs, lens):
            inp = get_inp_prog_path(p)
            out = get_out_prog_path(b, p)
            timing = get_out_timing_path(b, p)
            util = get_out_util_path(b, p)
            print("Compiling {} with [{}] backend...".format(inp, b))
            if b == "base":
                compile_ir_to_base(inp, out)
                compile_vivado("baseline", [out, timing, util])
            elif b == "hint":
                compile_ir_to_hint(inp, out)
                compile_vivado("baseline", [out, timing, util])
            elif b == "reticle":
                compile_ir_to_struct_placed(inp, out)
                compile_vivado("reticle", [out, timing, util])
            # data = update_time(data, b, l, elapsed)
    # df = pd.DataFrame.from_dict(data)
    # csv_name = "{}.csv".format(prog)
    # csv_path = os.path.join(
    #    get_scripts_dir(), "..", "data", "compiler", csv_name
    # )
    # df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    progs = ["tadd", "tdot", "fsm"]
    for p in progs:
        run(p)
    cleanup_vivado_files()
