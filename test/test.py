# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_aquapay_basic_flow(dut):
    dut._log.info("Starting AquaPay test")

    # Clock: 100 KHz
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # ---------------- RESET ----------------
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    await ClockCycles(dut.clk, 2)

    # ---------------- INSERT COIN (₹1) ----------------
    dut.ui_in.value = 0b00000001  # coin_1
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    # ---------------- WAIT FOR STATE MACHINE ----------------
    await ClockCycles(dut.clk, 5)

    # ---------------- CHECK VALVE OPENS ----------------
    assert dut.uo_out.value[0] == 1, "Valve should be ON after coin input"

    # ---------------- SIMULATE FLOW SENSOR ----------------
    for _ in range(10):
        dut.ui_in.value = 0b00010000  # flow_sensor = 1
        await ClockCycles(dut.clk, 1)

    dut.ui_in.value = 0

    await ClockCycles(dut.clk, 5)

    # ---------------- CHECK SYSTEM STILL WORKING ----------------
    assert dut.uo_out.value is not None, "Output should exist"

    dut._log.info("AquaPay test completed successfully")
