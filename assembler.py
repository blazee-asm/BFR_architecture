
import sys, os

def process_hex(hex_str: str):
    """Processes a number with format 0x... into bytes."""
    
    hex_str = hex_str.lower().lstrip("-")
    assert hex_str.startswith("0x"), "Hey, this isn't a hex number!"
    hex_str = hex_str[2:]
    
    if len(hex_str) % 2 == 1:
        hex_str = "0" + hex_str
    
    return bytes.fromhex(hex_str), len(hex_str) // 2

CONVERSIONS = {
    "label": b"\x00",
    "org": b"\x12",
    "cmp": b"\x4A",
    "jmp": b"\x4B",
    "jmpc": b"\x4C",
    "ret": b"\x4D",
    "inc": b"\x60",
    "dec": b"\x61",
    "zero": b"\x62",
    "mov": b"\x8C",
    "movq": b"\x8D",
    "movh": b"\x8E",
    "movr": b"\x8F",
    "lod": b"\x70",
    "sto": b"\x71",
    "int": b"\x86",
    "hlt": b"\xFF",
    "ax": b"\x10",
    "ax1": b"\x11",
    "ax2": b"\x12",
    "ax3": b"\x13",
    "ax4": b"\x14",
    "bx":  b"\x20",
    "bx1": b"\x21",
    "bx2": b"\x22",
    "bx3": b"\x23",
    "bx4": b"\x24",
    "cx":  b"\x30",
    "cx1": b"\x31",
    "cx2": b"\x32",
    "cx3": b"\x33",
    "cx4": b"\x34",
    "dx":  b"\x40",
    "dx1": b"\x41",
    "dx2": b"\x42",
    "dx3": b"\x43",
    "dx4": b"\x44",
    "i0": b"\x50",
    "i1": b"\x51",
    "i2": b"\x52",
    "i3": b"\x53",
}

REG_SIZES = {
    "ax": 32, "bx": 32, "cx": 32, "dx": 32,
    "ax1": 8, "ax2": 8, "ax3": 8, "ax4": 8,
    "bx1": 8, "bx2": 8, "bx3": 8, "bx4": 8,
    "cx1": 8, "cx2": 8, "cx3": 8, "cx4": 8,
    "dx1": 8, "dx2": 8, "dx3": 8, "dx4": 8,
    "i0": 1, "i1": 1, "i2": 1, "i3": 1,
}

labels = {}

pc = 0
inp_file = sys.argv[1]
out_file = sys.argv[2]
assert os.path.exists(inp_file), "Input file non-existent."
assert out_file.endswith(".bin"), "Invalid output file, must be .bin."

with open(inp_file) as f:
    code = [line.strip() for line in f.read().splitlines() if line.strip()]

with open(out_file, "wb") as f:
    # label pass
    line_num = 1
    while 0 <= line_num <= len(code):
        parts = code[line_num - 1].split(" ", 1)

        params = []
        if len(parts) > 1:
            params = parts[1].split(", ")

        if parts[0] == "label":
            labels[params[0]] = int.to_bytes(pc, 8, "big")

        pc += 1
        for param in params:
            if param.startswith("0x"):
                hex_num = process_hex(param)
                pc += hex_num[1]
                f.write(hex_num[0])
            elif labels.get(param):
                f.write(labels[param])
            else:
                assert REG_SIZES.get(param), f"line:{line_num} Invalid register."
                num_length = REG_SIZES[param]
                pc += num_length
                assert CONVERSIONS.get(param), f"line:{line_num} Invalid operand, not in mnemonic set."
                f.write(CONVERSIONS[param])
        
        line_num += 1
    # bytecode pass
    line_num = 1
    while 0 <= line_num <= len(code):
        parts = code[line_num - 1].split(" ", 1)
        instr = parts[0]
        assert CONVERSIONS.get(instr), f"line:{line_num} Invalid instruction."

        params = []
        if len(parts) > 1:
            params = parts[1].split(", ")

        if CONVERSIONS[instr] == b"\x00":
            line_num += 1
            continue
        f.write(CONVERSIONS[instr])
        pc += 1
        for param in params:
            if param.startswith("0x"):
                hex_num = process_hex(param)
                pc += hex_num[1]
                f.write(hex_num[0])
            elif labels.get(param):
                f.write(labels[param])
            else:
                assert REG_SIZES.get(param), f"line:{line_num} Invalid register."
                num_length = REG_SIZES[param]
                pc += num_length
                assert CONVERSIONS.get(param), f"line:{line_num} Invalid operand, not in mnemonic set."
                f.write(CONVERSIONS[param])

        line_num += 1
