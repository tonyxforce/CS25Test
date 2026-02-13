import sys
import glob
import serial
import time

import turtle

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


if __name__ == '__main__':
    with serial.Serial(serial_port()) as ser:
        with open(f"logs/AS/{time.time()}.txt", "a") as f:
            while True:
                line = ser.readline().decode('utf-8').strip()

                print(line)
                f.write(line + "\n")