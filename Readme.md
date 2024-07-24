# Coroutine Co-Simulation Test Bench (COCOTB)
This repository contains materials, simulations and other related documents on Coroutine Co-Simulation Test Bench (COCOTB). 

# Installation
Cocotb installation documentations can be found here [COCOTB Installation](https://docs.cocotb.org/en/stable/install.html). The installation procedure here is for Ubuntu; the installation procedure goes like this: procedure statements, followed by the shell scripts to be executed.

## Icarus Verilog and GTKWave
Before the installation begins, install **Icarus Verilog** and **GTKWave** `sudo apt-get install iverilog gtkwave`. These tools will be used in the examples for verification of the RTL design.

## Python and Python Package Installer
Check the **Python Version** installed `python --version` and proceed to install the latest version of Python and `pip` (Python Package Installer) by running the following script `sudo apt-get install python 3 python3-pip`. 

## Virtual Environment
Installation of COCOTB needs a virtual environment. Activating a virtual environment modifies the shell's environment so that when Python scripts or `pip` is used, they operate within the context of the virtual environment rather than the system-wide Python installation. 

Creating a virtual environment allows you to manage a separate package installation for different projects. `venv` creates a virtually isolated Python installation for COCOTB.

To create the virtual environment, run `pip3 -m venv venv` this creates a virtual environment named `venv` using the `pip3` command. Also, run `python3 -m venv venv` this is the standard method using Python 3's `venv` module to create a virtual environment named `venv`.

**CHECK** <br/>
To ensure the creation of a virtual environment, exit the virtual environment and, using the `ls` command, check the path folder.

Run `which python3` to locate where the Python 3 executable is installed in the system. It prints the path to the Python 3 executables. 

Then to invoke the virtual environment use the following scipt `source venv/bin/activate`. This command activates a Python virtual environment named `venv` that you previously created. 

## Installing COCOTB Packages
Running the following script installs several packages related to COCOTB (Coroutine-based Co-Simulation TestBench) using `pip3`, the Python package installer for Python 3.

```sh
pip3 install pytest cocotb cocotb-bus cocotb-coverage
```

|Package |Purpose |
|-----| ---- |
|`pytest`|A testing framework for Python that is commonly used with COCOTB to run test cases.|
|`cocotb`|The main COCOTB package that provides the core functionality for writing and running Python-based testbenches for HDL designs.|
|`cocotb-bus`|An extension for COCOTB that provides bus functional models (BFMs) for common bus protocols (e.g., AXI, Avalon).|
|`cocotb-coverage` |An extension for COCOTB that adds support for functional coverage analysis in testbenches.|

**CHECK**
```sh
ls venv/lib/python3.11/site-packages/
```
The above command lists the contents of the site-packages directory within your Python virtual environment (`venv`). This directory contains all the Python packages and modules installed into the virtual environment.

# COCOTB based Verification
## Combinational Circuits
### Verilog 
Save the files as `or_gate.v`
```verilog
module or_gate
(
	input a,
	input b,
	output y
);
assign y = a | b;
endmodule
```

### Python based TestBench (COCOTB)
Save the file as `or_test.py`
```python
import cocotb
from cocotb.triggers import Timer, RisingEdge

@cocotb.test()					# Decorator
async def or_test(dut):
	
	a = (0, 0, 1, 1)
	b = (0, 1, 0, 1)
	y = (0, 1, 1, 1)
	
	for i in range(4):
		dut.a.value = a[i]
		dut.b.value = b[i]
		await Timer (1, 'ns')
		
		assert dut.y.value == y[i], f"Error at Iteration {i}"
```

### Running using Makefile
To simulation is performed using a `Makefile`. The `Makefile` automate the compilation and execution of programs and other tasks in a software project run on Unix-based operating systems. To create the `Makefile` run the following command:
```sh
touch Makefile
```
Append the `Makefile` with the following contents
```make
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
PWD = $(shell pwd)
VERILOG_SOURCES += $(PWD)/or_gate.v

TOPLEVEL := or_gate
MODULE := or_test

include $(shell cocotb-config --makefiles)/Makefile.sim
```
Compile the Verilog file using the command `iverilog -o or_gate or_gate.v` and then run the simulation using the command `vvp or_gate`. Then in the terminal just type `make` to run the verification of the OR GATE.

### Result
|![image](https://github.com/user-attachments/assets/dcf764d8-87da-4db3-8162-8cbef5c70d9e)|
|:-:|
|_Figure 1. Simulation Result_|

### Verilog
Here is the verification of another combinational circuit, MUX2x1. Save the file as `mux.v`.
```verilog
module mux_2x1 
(
	input a, b, sel,
	output y
);
	assign y = sel ? a : b;
	initial begin
		$dumpfile("dump.vcd");
		$dumpvars(0, mux_2x1);	
	end
endmodule
```

### Python based TestBench (COCOTB)
Save the file as `test_mux.py`.
```python
import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure

@cocotb.test()
async def mux_test(dut):

    dut._log.info('start of test!')
    await Timer(1, 'ns')

    dut.a.value = 0
    dut.b.value = 0

    dut._log.info('Drive 0 to a & b inputs of 2x1 mux')
    await Timer(1, 'ns')

    dut.a.value = 1
    dut.sel.value = 1
    dut._log.info('Drive 1 to a & sel inputs of 2x1 mux')
    await Timer(1, 'ns')

    if dut.y.value != 1:
        raise TestFailure('Result is incorrect. %s !=1' %str(dut.y))
    else:
        dut._log.info('PASS !')

    dut.sel.value = 0
    dut._log.info('Drive 0 to sel inputs of 2x1 mux') 
    await Timer(1, 'ns')

    if dut.y.value != 0:
        raise TestFailure('Result is incorrect. %s !=0' %str(dut.y))
    else:
        dut._log.info('PASS !')
```
### Running using Makefile
```make
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
PWD = $(shell pwd)
VERILOG_SOURCES += $(PWD)/mux.v

TOPLEVEL := mux_2x1
MODULE := test_mux

include $(shell cocotb-config --makefiles)/Makefile.sim
```
Compile the Verilog file using the command `iverilog -o mux mux.v` and then run the simulation using the command `vvp mux`. A `dump.vcd` file is also created along with the binary mux file. Then in the terminal just type `make` to run the verification of the MUX.

### Results
|![image](https://github.com/user-attachments/assets/67543e10-0417-4b3e-982d-948f92b3fd6b)|
|:-:|
|_Figure 2. MUX Simulation Result_ |

Double click on `dump.vcd` file. Append the signals to the `signal` pane to view the output waveform.
|![image](https://github.com/user-attachments/assets/85ff0d5e-c011-46c1-bd11-384eb9f15e3a)|
|:-:|
|_Figure 3. Output Waveform_ |
