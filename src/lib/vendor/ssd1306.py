# Modified MicroPython SSD1306 OLED driver

from micropython import const
import framebuf

CONTRAST = const(0x81)
ENTIRE_ON = const(0xA4)
NORM_INV = const(0xA6)
DISP = const(0xAE)
MEM_ADDR = const(0x20)
COL_ADDR = const(0x21)
PAGE_ADDR = const(0x22)
DISP_START_LINE = const(0x40)
SEG_REMAP = const(0xA0)
MUX_RATIO = const(0xA8)
COM_OUT_DIR = const(0xC0)
DISP_OFFSET = const(0xD3)
COM_PIN_CFG = const(0xDA)
DISP_CLK_DIV = const(0xD5)
PRECHARGE = const(0xD9)
VCOM_DESEL = const(0xDB)
CHARGE_PUMP = const(0x8D)

WIDTH = const(64)
HEIGHT = const(48)
EXT_VCC = False
I2C_ADDR = const(0x3C)
PAGES = const(HEIGHT // 8)

class SSD1306(framebuf.FrameBuffer):
    def __init__(self, i2c):
        self.i2c = i2c
        self.tmp = bytearray(2)
        self.out = [b"\x40", None]  # Co=0, D/C#=1
        self.buf = bytearray(8)
        super().__init__(self.buf, 8, 8, framebuf.MONO_VLSB)
        for cmd in (
            DISP | 0x00,  # off
            # address setting
            MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            DISP_START_LINE | 0x00,
            SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            MUX_RATIO,
            HEIGHT - 1,
            COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            DISP_OFFSET,
            0x00,
            COM_PIN_CFG,
            0x02 if WIDTH > 2 * HEIGHT else 0x12,
            # timing and driving scheme
            DISP_CLK_DIV,
            0x80,
            PRECHARGE,
            0x22 if EXT_VCC else 0xF1,
            VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            CONTRAST,
            0xFF,  # maximum
            ENTIRE_ON,  # output follows RAM contents
            NORM_INV,  # not inverted
            # charge pump
            CHARGE_PUMP,
            0x10 if EXT_VCC else 0x14,
            DISP | 0x01,
        ):  # on
            self.cmd(cmd)

    def rst(self):
        # displays with width of 64 pixels are shifted by 32
        ost = 32 if WIDTH == 64 else 0
        self.cmd(COL_ADDR)
        self.cmd(ost)
        self.cmd(WIDTH - 1 + ost)
        self.cmd(PAGE_ADDR)
        self.cmd(0)
        self.cmd(PAGES - 1)

    def txt(self, txt):
        for c in txt:
            self.fill(0)
            self.text(c, 0, 0)
            self.dmp(self.buf)

    def cmd(self, cmd):
        self.tmp[0] = 0x80  # Co=1, D/C#=0
        self.tmp[1] = cmd
        self.i2c.writeto(I2C_ADDR, self.tmp)

    def dmp(self, buf):
        self.out[1] = buf
        self.i2c.writevto(I2C_ADDR, self.out)
