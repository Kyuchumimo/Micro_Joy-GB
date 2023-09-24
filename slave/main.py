# init
import zlib

# update
def u():
    hex_val = 0
    for i, pin in enumerate(btnmap):
        hex_val |= (pin.value() << i)

    print(f"0x{hex_val:02x}")

# draw
def d(ba):
    fb.fill(0)
    fb.blit(framebuf.FrameBuffer(bytearray.fromhex(zlib.decompress(ba)), 64, 48, framebuf.MONO_VLSB), 10, 0, 0)
    lcd.data(buffer)
    