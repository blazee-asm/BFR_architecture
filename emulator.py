
import sys, os, msvcrt

class Reg256:
    def __init__(self):
        self.parts = [0, 0, 0, 0]

    def read(self):
        return (self.parts[0] << 192) + (self.parts[1] << 128) + (self.parts[2] << 64) + self.parts[3]

    def write(self, value):
        self.parts = [
            (value >> 192) & 0xFFFFFFFFFFFFFFFF,
            (value >> 128) & 0xFFFFFFFFFFFFFFFF,
            (value >> 64) & 0xFFFFFFFFFFFFFFFF,
            value & 0xFFFFFFFFFFFFFFFF
        ]

class Reg8:
    def __init__(self):
        self.val = 0

    def read(self):
        return self.val
    
    def write(self, value):
        self.val = value & 0xFF

def compare_to_flag(a: int, b: int):
    if a < b: return 0x01
    if a == b: return 0x02
    if a > b: return 0x03

def list_64bit_to_256bit(nums: list):
    return (nums[0] << 196) + (nums[1] << 128) + (nums[2] << 64) + nums[3]

def parse_size(size_str: str):
    units = {"b": 1, "k": 1024, "m": 1024**2, "g": 1024**3}
    size_str = size_str.lower().strip()
    if size_str[-1] in units:
        return int(size_str[:-1]) * units[size_str[-1]]
    return int(size_str)

def concat_to_hex(a: list):
    hex_str = ''.join(f'{b:02x}' for b in a)
    return int(hex_str, 16)

def get_last_hex_digit(a: int):
    return a & 0xF

def hex_to_reg_val(a: int):
    if REGISTERS_256.get(a):
        return registers[REGISTERS_256.get(a)].read()
    elif REGISTERS_64.get(a):
        return registers[REGISTERS_64.get(a)][get_last_hex_digit(a) - 1].read()
    elif REGISTERS_8.get(a):
        return registers[REGISTERS_8.get(a)].read()

def write_to_reg(a: int, b: int):
    if REGISTERS_256.get(a):
        registers[REGISTERS_256.get(a)].write(b)
    elif REGISTERS_64.get(a):
        registers[REGISTERS_64.get(a)][get_last_hex_digit(a) - 1].write(b)
    elif REGISTERS_8.get(a):
        registers[REGISTERS_8.get(a)].write(b)

REGISTERS_256 = {
    0x10: "ax",
    0x20: "bx",
    0x30: "cx",
    0x40: "dx",
}

REGISTERS_64 = {
    0x11: "ax",
    0x21: "bx",
    0x31: "cx",
    0x41: "dx",
    0x12: "ax",
    0x22: "bx",
    0x32: "cx",
    0x42: "dx",
    0x13: "ax",
    0x23: "bx",
    0x33: "cx",
    0x43: "dx",
    0x14: "ax",
    0x24: "bx",
    0x34: "cx",
    0x44: "dx",
}

REGISTERS_8 = {
    0x50: "i0",
    0x51: "i1",
    0x52: "i2",
    0x53: "i3",
}

registers = {
    "ax": Reg256(),
    "bx": Reg256(),
    "cx": Reg256(),
    "dx": Reg256(),
    "i0": Reg8(),
    "i1": Reg8(),
    "i2": Reg8(),
    "i3": Reg8(),
}
flag: int
ret_reg: bytes
pc, origin = 0, 0

inp_file = sys.argv[1]
ram_alloc = parse_size(sys.argv[2])
assert os.path.exists(inp_file), "File non-existent."
assert inp_file.endswith(".bin"), "File not of proper extension."

ram = bytearray(ram_alloc)

import sys
assert sys.version_info >= (3, 10), "Error: Python 3.10+ is required to run this emulator."

with open(inp_file, "rb") as f:
    code = f.read()
    if code[0] == 0x12:
        pc = int.from_bytes(code[1:5])
        origin = pc
    for offset, byte in enumerate(code):
        ram[offset + pc] = byte
    code = None # so the code variable stops taking up RAM
    pc += 5

while True:
    opcode = ram[pc]
    print(f"PC={pc} opcode=0x{opcode:02x}")
    if opcode == 0x4a:
        reg, val = hex_to_reg_val(ram[pc + 1]), 0
        if REGISTERS_256.get(ram[pc + 1]):
            val = int.from_bytes(ram[pc + 2:pc + 34])
            pc += 34
        elif REGISTERS_64.get(ram[pc + 1]):
            val = int.from_bytes(ram[pc + 2:pc + 10])
            pc += 10
        elif REGISTERS_8.get(ram[pc + 1]):
            val = ram[pc + 2]
            pc += 3
        flag = compare_to_flag(reg, val)
    elif opcode == 0x4b:
        addr_bytes = ram[pc + 1:pc + 9]
        addr = int.from_bytes(addr_bytes, signed=True)
        ret_reg = int.to_bytes(pc + 9, 8)
        pc = addr + origin
        continue
    elif opcode == 0x4c:
        if flag != ram[pc + 1]:
            pc += 10
            continue
        addr_bytes = ram[pc + 2:pc + 10]
        addr = int.from_bytes(addr_bytes, signed=True)
        ret_reg = int.to_bytes(pc + 10, 8)
        pc = addr + origin
        continue
    elif opcode == 0x4d:
        pc = int.from_bytes(ret_reg)
        continue
    elif opcode == 0x60:
        write_to_reg(ram[pc + 1], hex_to_reg_val(ram[pc + 1]) + 1)
    elif opcode == 0x61:
        write_to_reg(ram[pc + 1], hex_to_reg_val(ram[pc + 1]) - 1)
    elif opcode == 0x62:
        write_to_reg(ram[pc + 1], 0)
    elif opcode == 0x70:
        if REGISTERS_64.get(ram[pc + 2]): addr = hex_to_reg_val(ram[pc + 2])
        else: addr = int.from_bytes(ram[pc + 2:pc + 10])
        write_to_reg(ram[pc + 1], ram[addr])
        pc += 3 if REGISTERS_64.get(ram[pc + 2]) else 10
    elif opcode == 0x71:
        addr = hex_to_reg_val(ram[pc + 1])
        ram[addr] = hex_to_reg_val(ram[pc + 2]) & 0xFF
        pc += 3
    elif opcode == 0x86:
        interrupt_id = ram[pc + 1]
        if interrupt_id == 0xa0:
            val = registers["i0"].read()
            print(f"Printing char: {chr(val) if val >= 32 else repr(val)}")
            if val == 0x0d: print()
            elif val == 0x08:
                print("\b \b", end="", flush=True)
            else: print(chr(val), end="", flush=True)
        elif interrupt_id == 0xa1:
            print(end="", flush=True)
            registers["i0"].write(int.from_bytes(msvcrt.getch()))
            val = registers["i0"].read()
            if val == 0xe0 or val == 0x00:
                registers["i1"].write(int.from_bytes(msvcrt.getch()))
        elif interrupt_id == 0x4f: os.system("cls")
        pc += 2
    elif opcode == 0x8c:
        write_to_reg(ram[pc + 1], ram[pc + 2])
        pc += 3
    elif opcode == 0x8d:
        val = int.from_bytes(ram[pc + 2:pc + 10])
        write_to_reg(ram[pc + 1], val)
        pc += 10
    elif opcode == 0x8e:
        val = int.from_bytes(ram[pc + 2:pc + 34])
        reg = REGISTERS_256[ram[pc + 1]]

        registers[reg].write(val)
        pc += 34
    elif opcode == 0x8f:
        reg1, reg2 = REGISTERS_256.get(ram[pc + 1]), REGISTERS_256.get(ram[pc + 2])
        globals()[reg1] = globals()[reg2]
        pc += 3
    
    if pc >= ram_alloc or pc < 0:
        break
