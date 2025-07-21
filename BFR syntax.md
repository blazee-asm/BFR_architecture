
# BFR Syntax
You probably installed this to work in a lightweight assembly, right? I'm reading your mind.
So here's the instruction set + their bytecode counterparts.
## Registers
`ax`/0x10 - A 256-bit register split into 4 64-bit quadrants, called ax1, ax2, ax3, ax4, where ax1 is the most significant (highest value) quadrant.
`bx`/0x20 - Just ax but with a B instead of an A.
`cx`/0x30 - Just ax but with a C instead of an A.
`dx`/0x40 - Just ax but with a D instead of an A.
`i0, i1, i2, i3`/0x50, 0x51, 0x52, 0x53 respectively - 8-bit registers for BIOS interrupts.
## Non-bytecode Instructions
`label` - Defines a label which can be used later in various instructions. - label some_label
## Conditional Instructions
`jmp`/0x4b - Unconditional jump to a label or address, and also sets a return register. - jmp some_label
`jmpc`/0x4c - Conditional jump depending on flag, and also sets a return register. - jmp 0x02, some_other_label
`cmp`/0x4a - Compares a register to a value, and sets the flag register. 0x01 if less than, 0x02 if equal, 0x03 if greater than. - cmp ax1, 0
`ret`/0x4d - Returns to the address given in the return register. - ret
## Register Operations
`movh`/0x8e - Moves an entire hexaword (256-bit value) to a 256-bit register. - movh ax, 0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
`movq`/0x8d - Moves a quadword (64-bit value) to a quadrant of each 256-bit register. - movq ax1, 0x00000000deadbeef
`mov`/0x8c - Moves a byte to an 8-bit register. - mov i0, 0x41
`movr`/0x8f - Moves the second register's value into the first one. - movr ax2, ax1
`inc`/0x60 - Increments any register. - inc ax
`dec`/0x61 - Decrements any register. - dec bx3
`zero`/0x62 - Zeroes out any register. - zero cx4
## Memory Operations
`lod`/0x70 - Loads allocated RAM at an address (can be inside a register, direct address must be 8 bytes) and writes it into a different one. - lod i0, 0x00000000cafebabe
`sto`/0x71 - Stores what's in one register (last byte of the value) into allocated RAM at address of a second register. - sto i1, ax2
`db`/0x72 - Writes bytes to RAM. (in ASCII, *0x68656c6c6f* is *"hello"*) - db 0x68656c6c6f
## Interrupts
`int`/0x86 - Interrupts with a given ID.
Interrupt IDs:
* 0xa0 - Outputs the contents of i0 to the terminal. - int 0xa0
* 0xa1 - Gets a keypress. Keys like Delete are stored in i1, while printable keys are in i0. - int 0xa1
* 0xaf - Clears the terminal. - int 0xaf
## Other Instructions
`org`/0x12 - Sets where in the allocated RAM the script should start (4-byte address) - org 0x00000000
`hlt`/0xff - Halts the program. - hlt
# Example Script
```
org 0x00000000
label start
int 0xa1
int 0xa0
jmp start
```