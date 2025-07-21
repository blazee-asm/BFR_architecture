
# The BFR Computing Architecture
This is an original computing architecture emulated in Python.
BFR stands for **Big Fat Registers**, because BFR's registers are big, wide, 32-byte chunks of numbers.
## Setup
* Prior to running BFR code, install any *Python 3.10+* application on the Microsoft Store (preferably Python 3.13).
▶️ [Watch install_python.mp4](./videos/install_python.mp4)
* Afterwards, go to your BFR folder in the File Explorer, press Alt+D and enter cmd.
▶️ [Watch cmd_at_bfr.mp4](./videos/cmd_at_bfr.mp4)
* Now, you have cmd open at your folder. Enter this into that command prompt: **.\bfr-emul binary/hello.bin 256M**.
## Arguments
Emulator arguments:
.\bfr-emul \<file\> \<ram-allocation\>
* \<file\>: a file with extension .bin. Assembled using your BFR assembler.
* \<ram-allocation\>: how many bytes (b), kilobytes (k), megabytes (m), or gigabytes (g) of RAM (not disk) to use for your BFR programs. example: 256m.