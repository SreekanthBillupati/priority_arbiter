from __future__ import annotations

import os
import random
from pathlib import Path
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb_tools.runner import get_runner


@cocotb.test()
async def test_priority_arbiter(dut):
    """Test priority arbiter with known input/output pairs"""
    
    # Start the clock (10ns period = 100MHz)
    clock = Clock(dut.clk_i, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Apply reset
    dut.rstn_i.value = 0
    await RisingEdge(dut.clk_i)
    await RisingEdge(dut.clk_i)
    dut.rstn_i.value = 1
    await RisingEdge(dut.clk_i)
    
    # Test cases: (req_i, expected_gnt_o)
    test_vectors = [
        (0b0000, 0b0000),  # No request -> No grant
        (0b0001, 0b0001),  # Request bit 0 -> Grant bit 0 (highest priority)
        (0b0010, 0b0010),  # Request bit 1 -> Grant bit 1
        (0b0100, 0b0100),  # Request bit 2 -> Grant bit 2
        (0b1000, 0b1000),  # Request bit 3 -> Grant bit 3 (lowest priority)
        (0b0011, 0b0001),  # Multiple requests -> Grant highest priority (bit 0)
        (0b1111, 0b0001),  # All requests -> Grant bit 0
        (0b1110, 0b0010),  # Requests 1,2,3 -> Grant bit 1
        (0b1100, 0b0100),  # Requests 2,3 -> Grant bit 2
        (0b0101, 0b0001),  # Requests 0,2 -> Grant bit 0
    ]
    
    # Run through test vectors
    for req, expected_gnt in test_vectors:
        dut.req_i.value = req
        await RisingEdge(dut.clk_i)
        await Timer(1, units="ns")  # Small delay for signal propagation
        
        actual_gnt = dut.gnt_o.value.integer
        
        if actual_gnt != expected_gnt:
            dut._log.error(
                f"FAIL: req_i=0b{req:04b}, expected gnt_o=0b{expected_gnt:04b}, "
                f"got gnt_o=0b{actual_gnt:04b}"
            )
            assert False, f"Mismatch for req_i=0b{req:04b}"
        else:
            dut._log.info(
                f"PASS: req_i=0b{req:04b} -> gnt_o=0b{actual_gnt:04b}"
            )
    
    dut._log.info("All test vectors passed!")


def test_priority_arbiter_hidden_runner():

    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    sources = [proj_path / "golden/priority_arbiter.v"]
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="priority_arbiter",
        always=True,
    )

    runner.test(hdl_toplevel="priority_arbiter", test_module="test_priority_arbiter_hidden")