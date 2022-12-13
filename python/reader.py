import argparse, sys
import signal
import serial

from sklearnex import patch_sklearn
patch_sklearn()

file_name = "collected"
device_number = 0
data = []

DEVICE_MAC = "/dev/tty.usbmodem"
DEVICE_LINUX = "/dev/ttyACM"

os = DEVICE_LINUX
def write_file():
    with open("../data/{}-{}.csv".format(file_name, device_number), "w") as f:
        f.write(''.join(data))
        f.close()

def handler(signum, frame):
    write_file()
    exit(0)

def main():
    ser = serial.Serial('{}{}'.format(os, device_number))
    while(1):
        line = ser.readline()
        print(line)
        data.append(line.decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", help = "Unique device number in '/dev/ttyACM\{\}'")
    parser.add_argument("--file", help="Output file name '\{\}.csv'")
    parser.add_argument("--os", help="l for linux, m for mac")

    args = parser.parse_args()

    if args.device is not None:
        device_number = args.device
    if args.file is not None:
        file_name = args.file
    if args.os is not None and args.os == "m":
        os = DEVICE_MAC
    print(device_number)
    print(file_name)
    print(os)
    signal.signal(signal.SIGINT, handler)
    main()



