import sys
import glob
import serial
import time

import turtle

PIXELSIZE = 50

t = turtle.Turtle()
turtle.tracer(0, 0)
screen = turtle.Screen()
t.penup();
t.speed(0);
t.hideturtle();
t.goto(-PIXELSIZE*4, PIXELSIZE*4)

import math
def convert_K_to_RGB(colour_temperature):
    """
    Converts from K to RGB, algorithm courtesy of 
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    #range check
    if colour_temperature < 1000: 
        colour_temperature = 1000
    elif colour_temperature > 40000:
        colour_temperature = 40000
    
    tmp_internal = colour_temperature / 100.0
    
    # red 
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = tmp_red
    
    # green
    if tmp_internal <=66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    
    # blue
    if tmp_internal >=66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = tmp_blue
    
    return red, green, blue

def serial_port():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            return port
        except (OSError, serial.SerialException):
            pass

def leftPad(s):
    while len(s) < 2:
        s = "0" + s
    return s

def setColorRGB(color):
    r,g,b = color
    t.fillcolor("#"+
                leftPad(hex(int(r))[2:])
                +leftPad(hex(int(g))[2:])
                +leftPad(hex(int(b))[2:]))

def chunks(xs, n):
    n = max(1, n)
    return (xs[i:i+n] for i in range(0, len(xs), n))


if __name__ == '__main__':
    with serial.Serial(serial_port()) as ser:
        with open(f"logs/AMG/{time.time()}.txt", "a") as f:
            while True:
                line = ser.readline().decode('utf-8').strip()
                ser.read_all() # Clear the buffer

                if(not line.startswith("|STAR|") or not line.endswith("|END|")): continue
                
                f.write(line + "\n")

                values = list(map(float, (line[6:-5]).split("|")))
                def divideBySmallest(inpt):
                    return inpt / max(values)
                
                if(len(values)< 3): continue

                #values = list(map(divideBySmallest, values))

                t.goto(-PIXELSIZE*4, PIXELSIZE*4)
                for row in chunks(values[::-1], 8):
                    for value in row[::-1]:
                        setColorRGB(convert_K_to_RGB((value)*200))
                        t.begin_fill()
                        for i in range(4):
                            t.forward(PIXELSIZE)
                            t.left(90)
                        t.end_fill()
                        t.forward(PIXELSIZE)
                    t.backward(PIXELSIZE*8)
                    t.right(90)
                    t.forward(PIXELSIZE)
                    t.left(90)
                turtle.update()
                turtle.clear()