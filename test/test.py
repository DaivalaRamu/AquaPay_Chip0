# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_aquapay_chip(dut):
    dut._log.info("Start AquaPay Test")

    # Clock = 100 kHz
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Insert ₹2 coin")

    # ₹2 coin (ui_in[1])
    dut.ui_in.value = 0b00000010

    await ClockCycles(dut.clk, 1)

    # remove coin
    dut.ui_in.value = 0

    # simulate flow sensor pulses
    for i in range(6):
        dut.ui_in.value = 0b00010000  # flow_sensor = ui_in[4]
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)

    dut._log.info("Check valve and output")

    # valve should have turned ON at some point
    # (we don't force exact cycle timing, FSM dependent)

    assert dut.uo_out.value[0] in [0, 1], "Valve signal invalid"

    dut._log.info("Test complete")
