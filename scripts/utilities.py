import os
import subprocess as sp


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


def update_time(data, backend, length, time):
    if data:
        data["backend"].append(backend)
        data["length"].append(length)
        data["time"].append(time)
    else:
        data["backend"] = [backend]
        data["length"] = [length]
        data["time"] = [time]
    return data


def get_scripts_dir():
    return os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))


def change_dir(path):
    os.chdir(path)


def make_dir(path):
    p = os.path.join(path)
    if not os.path.isdir(p):
        os.makedirs(p)


def make_source_dir(backend):
    source_dir = os.path.join(
        get_scripts_dir(), "..", "out", "sources", backend
    )
    make_dir(source_dir)


def get_inp_prog_path(name):
    filename = "{}.ir".format(name)
    return os.path.join(get_scripts_dir(), "..", "examples", filename)


def get_out_prog_path(backend, name):
    filename = "{}.v".format(name)
    return os.path.join(
        get_scripts_dir(), "..", "out", "sources", backend, filename
    )


def get_tcl_path(name):
    filename = "{}.tcl".format(name)
    return os.path.join(get_scripts_dir(), filename)


def compile_ir_to_base(inp, out):
    cmd = []
    cmd.append("reticle-translate")
    cmd.append(inp)
    cmd.append("-o")
    cmd.append(out)
    cmd.append("--fromto")
    cmd.append("ir-to-behav")
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


def compile_ir_to_hint(inp, out):
    cmd = []
    cmd.append("reticle-translate")
    cmd.append(inp)
    cmd.append("-o")
    cmd.append(out)
    cmd.append("--fromto")
    cmd.append("ir-to-behav-dsp")
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


def compile_ir_to_struct_placed(inp, out):
    cmd = []
    cmd.append("reticle-translate")
    cmd.append(inp)
    cmd.append("-o")
    cmd.append(out)
    cmd.append("--fromto")
    cmd.append("ir-to-struct-placed")
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


def compile_vivado(name, opts):
    tcl = get_tcl_path(name)
    cmd = []
    cmd.append("vivado")
    cmd.append("-mode")
    cmd.append("batch")
    cmd.append("-source")
    cmd.append(tcl)
    if opts:
        cmd.append("-tclargs")
        cmd = cmd + opts
    cp = sp.run(cmd, check=True, stdout=sp.PIPE)
    return cp.stdout.decode("utf-8")


def remove_files_with_ext(path, ext):
    root = os.listdir(path)

    for item in root:
        if item.endswith(".{}".format(ext)):
            os.remove(os.path.join(path, item))


def cleanup_vivado_files():
    path = os.path.join(get_scripts_dir(), "..")
    remove_files_with_ext(path, "jou")
    remove_files_with_ext(path, "log")
