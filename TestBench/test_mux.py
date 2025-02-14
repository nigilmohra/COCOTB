# Combinational Circuit
# Nigil

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

# -------------------------------------------------------------  
#                      2024 NIGIL M R
# -------------------------------------------------------------
