import time

# display
from machine import Pin, SPI
import pcd8544

spi = SPI(0, sck=Pin(18), mosi=Pin(19))
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin(21)
dc = Pin(20)
rst = Pin(22)
bl = Pin(17, Pin.OUT, value=1)
lcd = pcd8544.PCD8544(spi, cs, dc, rst)

import framebuf
buffer = bytearray((pcd8544.HEIGHT // 8) * pcd8544.WIDTH)
fb = framebuf.FrameBuffer(buffer, pcd8544.WIDTH, pcd8544.HEIGHT, framebuf.MONO_VLSB) 

def text_wrap(str,x,y,color,w,h,border=None):
    # optional box border
    if border is not None:
        fb.rect(x, y, w, h, border)
    cols = w // 8
    # for each row
    j = 0
    for i in range(0, len(str), cols):
        # draw as many chars fit on the line
        fb.text(str[i:i+cols], x, y + j, color)
        j += 8
        # dont overflow text outside the box
        if j >= h:
            break

fb.fill(0)
fb.blit(framebuf.FrameBuffer(bytearray(b'\x04\x11\x04\x11\x04'), 5, 5, framebuf.MONO_VLSB), 4, 21)
fb.text("MICRO JOY", 11, 20)
lcd.data(buffer)

# audio
import music76489

music = music76489.Music76489()

music.play_notes("SO4GGO5CEQG")

# input
btnmap = [machine.Pin(pin_num, machine.Pin.IN) for pin_num in range(8)]
btn = [False] * 8

def read_input():
    for i, pin in enumerate(btnmap):
        if not pin.value() and not btn[i]:
            btn[i] = True
            return i
        elif pin.value() and btn[i]:
            btn[i] = False
    return None
