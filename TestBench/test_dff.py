# -------------------------------------------------------------  
# SEQUENTIAL CIRCUIT | D FLIP FLOP | COCOTB TEST BENCH
# -------------------------------------------------------------

import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.result import TestFailure

@cocotb.test()
async def test_dff(dut):

    dut._log.info('Start of the test here')

    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    dut._log.info('Generating a clk of 10ns')

    for i in range(10):
        dut.d.value = random.randint(0, 1)
        await FallingEdge(dut.clk)  # random value at every negedge clk

    if dut.q.value != dut.d.value:
        raise TestFailure('Incorrect: %s dut.q.value != dut.q.value' % dut.q.value.binstr)
        print('Random value of d is', dut.d.value.binstr)
        print('Value of output q is', dut.q.value.binstr)
    else:
        dut._log.info('Correct')
        print('Random value of d is', dut.d.value.binstr)
        print('Value of output q is', dut.q.value.binstr)

    dut._log.info('End of test here')

# -------------------------------------------------------------  
#                      2024 NIGIL M R
# -------------------------------------------------------------