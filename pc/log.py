import sys
import glob
import serial
import time


def serial_port():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
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
    LIGHT_ON = True
    
    readingCount = 0
    with serial.Serial(serial_port()) as ser:
        with open(f"logs/{int(time.time())}.txt", "a") as f:
            f.write("|sensor|Tdelta|415nm|445nm|480nm|515nm|555nm|Clear| NIR |590nm|630nm|680nm|Clear| NIR |\n")
            print("|sensor|Tdelta|415nm|445nm|480nm|515nm|555nm|Clear| NIR |590nm|630nm|680nm|Clear| NIR |")
            if LIGHT_ON:
                ser.write(b" ");
            while True:
                line = ser.readline().decode('utf-8').strip()
                readingCount+=1
                f.write(line + "\n")
                print(line)
                f.write(line.replace("\r", "") + "\n")
                if(readingCount >= 50):
                    break;
            if LIGHT_ON:
                ser.write(b" ");