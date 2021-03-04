import argparse
import sys


def fmt(ident, value):
    return "{}{}".format(ident, value)


def expr(ident, ty):
    return "{}:{}".format(ident, ty)


def port(ident, index, ty):
    return expr(fmt(ident, index), ty)


def reg(ident, inp, en, ty):
    e = expr(ident, ty)
    return "{} = reg[0]({}, {});".format(e, inp, en)


def add(ident, lhs, rhs, ty):
    e = expr(ident, ty)
    return "{} = add({}, {});".format(e, lhs, rhs)


def signature(inps, outs):
    i = ", ".join(inps)
    o = ", ".join(outs)
    signature = "def main({})->({})".format(i, o)
    return signature


def prog(inps, outs, body):
    s = signature(inps, outs)
    b = "\n".join(body)
    prog = "{} {{\n{}\n}}".format(s, b)
    return prog


def emit(ty, length):
    en = "en"
    inps = []
    outs = []
    body = []

    inps.append(expr(en, "bool"))
    for i in range(length):
        pa = port("a", i, ty)
        pb = port("b", i, ty)
        py = port("y", i, ty)
        a = fmt("a", i)
        b = fmt("b", i)
        y = fmt("y", i)
        t0 = fmt("t", 3 * i)
        t1 = fmt("t", 3 * i + 1)
        t2 = fmt("t", 3 * i + 2)
        inps.append(pa)
        inps.append(pb)
        outs.append(py)
        body.append(reg(t0, a, en, ty))
        body.append(reg(t1, b, en, ty))
        body.append(add(t2, t0, t1, ty))
        body.append(reg(y, t2, en, ty))

    return prog(inps, outs, body)


def parse_args():
    parser = argparse.ArgumentParser(description="generator")
    parser.add_argument(
        "-p", help="prim type dsp-vector or lut-scalar", type=str
    )
    parser.add_argument("-l", help="length of vector", type=int)
    parser.add_argument("-o", help="output file", type=str)
    args = parser.parse_args()
    if not isinstance(args.p, str):
        print("Error: missing function name")
        parser.print_help(sys.stderr)
        sys.exit(1)
    if not isinstance(args.l, int):
        print("Error: missing length parameter")
        parser.print_help(sys.stderr)
        sys.exit(1)
    return args.p, args.l, args.o


if __name__ == "__main__":
    prim, length, output = parse_args()
    ty = "i8<4>" if prim == "dsp-vector" else "i8"
    assert length > 0, "length must be greater than zero"
    if prim == "dsp-vector":
        length % 4 == 0, "length must be a multiple of 4"
    length = length // 4 if prim == "dsp-vector" else length
    prog = emit(ty, length)
    if output:
        with open(output, "w") as file:
            file.write(prog)
    else:
        print(prog)
