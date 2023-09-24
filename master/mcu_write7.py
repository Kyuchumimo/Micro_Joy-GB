from pyboy import PyBoy
from pyboy import WindowEvent
from threading import Thread

import traceback
import time

import serial
from PIL import Image
import zlib

pilImage = Image.new('L', (0, 0))
u_data = 0xff

def runPyBoy():
    global pilImage

    keymap_p = (WindowEvent.PRESS_ARROW_UP, WindowEvent.PRESS_ARROW_DOWN, WindowEvent.PRESS_ARROW_LEFT, WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.PRESS_BUTTON_B, WindowEvent.PRESS_BUTTON_A, WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.PRESS_BUTTON_START)
    keymap_r = (WindowEvent.RELEASE_ARROW_UP, WindowEvent.RELEASE_ARROW_DOWN, WindowEvent.RELEASE_ARROW_LEFT, WindowEvent.RELEASE_ARROW_RIGHT, WindowEvent.RELEASE_BUTTON_B, WindowEvent.RELEASE_BUTTON_A, WindowEvent.RELEASE_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_START)

    with PyBoy('game.gb', disable_renderer=False, sound=True) as pyboy:
        while not pyboy.tick():
            pilImage = pyboy.screen_image()
            
            for i in range(8):
                current_status = not u_data & 1 << i  # invert the value, since we are using PULL_UP
                if current_status != previous_state[i]:
                    if current_status:
                        pyboy.send_input(keymap_p[i])
                    else:
                        pyboy.send_input(keymap_r[i])
                    previous_state[i] = current_status
            
            pass

ser = serial.Serial(
  port='COM3', # change this according to connection methods, e.g. /dev/ttyUSB0
  baudrate = 115200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

# going to raw
ser.write(str.encode("\r" + "\x03" + "\x03"));  # ctrl-C twice: interrupt any running program
ser.write(str.encode("\r" + "\x01"));

out1 = "T>> "
time.sleep(1)
while ser.inWaiting() > 0:
    out1 += bytes.decode(ser.read(1))
if out1 != '':
    print(str(out1))

def receive() -> str:
    return ser.readline().decode('utf-8').rstrip('\n')

def send(text: str) -> bool:
    ser.read_until(b">")
    
    ser.write(str.encode('%s\r\x04' % text))

    # check if we could exec command
    ret = ser.read(2)
    if ret != b"OK":
        raise Exception("could not exec command (response: %r)" % ret)

# list for storing the previous state of the buttons
previous_state = [False] * 8

def main():
    global u_data
    
    while True:
        start = time.time()
        
        # resize the image
        #pilImage.thumbnail((84, 48))
        img = pilImage.resize((64, 48))
        
        # converts the image to a mode
        img = img.convert("L") # use "L" for threshold mode and "1" for dithering mode

        # calculates the size of the data buffer
        width, height = img.size
        buffer_size = (width * ((height - 1) // 8 + 1))

        # initializes the data buffer
        d_data = bytearray(buffer_size)

        # iterates over the image pixels and updates the data buffer
        for y in range(height):
            for x in range(width):
                byte_index, bit_index = divmod(y, 8)
                pixel_value = img.getpixel((x, y))
                if pixel_value < 128: # threshold level
                    d_data[x + byte_index * width] |= 1 << bit_index
        
        send(f"d({zlib.compress(d_data.hex().encode(), 1)})")
        
        try:        
            send("u()")
            
            u_data = eval(receive())
        except (SyntaxError, UnicodeDecodeError, TypeError, serial.serialutil.SerialException):
            traceback.print_exc()
            time.sleep(1)
        
        print(f"FPS: {1/(time.time() - start)}")

Thread(target=runPyBoy).start()
Thread(target=main).start()
