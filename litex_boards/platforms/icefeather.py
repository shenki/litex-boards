#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2020 Piotr Esden-Tempski <piotr@esden.net>
# Copyright (c) 2021 Joel Stanley <joel@jms.id.au>
# SPDX-License-Identifier: BSD-2-Clause

# iCE40 Feather FPGA
# https://github.com/joshajohnson/iCE40-feather

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform
from litex.build.lattice.programmer import IceStormProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk12", 0, Pins("35"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led_n",    0, Pins("47"), IOStandard("LVCMOS33")), # nLED (red)

    # Leds
    ("user_led", 0, Pins("41"), IOStandard("LVCMOS33")), # rgb_led.r
    ("user_led", 1, Pins("40"), IOStandard("LVCMOS33")), # rgb_led.g
    ("user_led", 2, Pins("39"), IOStandard("LVCMOS33")), # rgb_led.b
    ("rgb_led", 0,
        Subsignal("r", Pins("41"), IOStandard("LVCMOS33")),
        Subsignal("g", Pins("40"), IOStandard("LVCMOS33")),
        Subsignal("b", Pins("39"), IOStandard("LVCMOS33")),
    ),

    # Serial
    ("serial", 0,
        Subsignal("rx", Pins("23")),
        Subsignal("tx", Pins("21"), Misc("PULLUP")),
        IOStandard("LVCMOS33")
    ),

    # SPIFlash
    ("spiflash", 0,
        Subsignal("cs_n", Pins("16"), IOStandard("LVCMOS33")),
        Subsignal("clk",  Pins("15"), IOStandard("LVCMOS33")),
        Subsignal("miso", Pins("17"), IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("14"), IOStandard("LVCMOS33")),
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("GPIO", "25 26 27 28 36 31 32 37 38 43 44 48 2 3 4 6 9 10 11 12 46 13 42 45"),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(LatticePlatform):
    default_clk_name   = "clk12"
    default_clk_period = 1e9/12e6

    def __init__(self, toolchain="icestorm"):
        LatticePlatform.__init__(self, "ice40-up5k-sg48", _io, _connectors, toolchain=toolchain)

    def create_programmer(self):
        return IceStormProgrammer()

    def do_finalize(self, fragment):
        LatticePlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk12", loose=True), 1e9/12e6)
