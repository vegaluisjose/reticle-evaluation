import os
from utilities import *
from time import perf_counter
import pandas as pd


def get_prog_len(prog):
    if prog == "tadd":
        return [64, 128, 256, 512]
    elif prog == "tdot":
        return [0, 1, 2, 3]
    elif prog == "fsm":
        return [3, 5, 7, 9]
    else:
        return []


def get_prog_list(prog):
    if prog == "tadd":
        return ["tadd_64", "tadd_128", "tadd_256", "tadd_512"]
    elif prog == "tdot":
        return ["tdot_5_3", "tdot_5_9", "tdot_5_18", "tdot_5_36"]
    elif prog == "fsm":
        return ["fsm_3", "fsm_5", "fsm_7", "fsm_9"]
    else:
        return []


def update(data, backend, length, time):
    if data:
        data["backend"].append(backend)
        data["length"].append(length)
        data["time"].append(time)
    else:
        data["backend"] = [backend]
        data["length"] = [length]
        data["time"] = [time]
    return data


def run(prog):
    backends = ["base", "hint", "reticle"]
    progs = get_prog_list(prog)
    lens = get_prog_len(prog)
    data = {}
    for b in backends:
        make_source_dir(b)
        for p, l in zip(progs, lens):
            inp = get_inp_prog_path(p)
            out = get_out_prog_path(b, p)
            print("Compiling {} with [{}] backend...".format(inp, b))
            if b == "base":
                compile_ir_to_base(inp, out)
                start = perf_counter()
                compile_vivado("synth_place", [out])
                elapsed = perf_counter() - start
            elif b == "hint":
                compile_ir_to_hint(inp, out)
                start = perf_counter()
                compile_vivado("synth_place", [out])
                elapsed = perf_counter() - start
            elif b == "reticle":
                start = perf_counter()
                compile_ir_to_struct_placed(inp, out)
                elapsed = perf_counter() - start
            print("Compilation time: {} seconds...".format(elapsed))
            data = update(data, b, l, elapsed)
    df = pd.DataFrame.from_dict(data)
    csv_name = "{}.csv".format(prog)
    csv_path = os.path.join(
        get_scripts_dir(), "..", "data", "compiler", csv_name
    )
    df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    progs = ["tadd", "tdot", "fsm"]
    for p in progs:
        run(p)
    cleanup_vivado_files()
