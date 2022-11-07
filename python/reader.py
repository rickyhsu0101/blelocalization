import argparse, sys
import signal
import serial


file_name = "collected"
device_number = 0
data = []
def write_file():
    with open("../data/{}.csv".format(file_name), "w") as f:
        for line in data:
            f.write(line + "\n")
        f.close()

def handler(signum, frame):
    write_file()
    exit(0)

def main():
    ser = serial.Serial('/dev/ttyACM{}'.format(device_number))
    while(1):
        line = ser.readline()
        data.append(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", help = "Unique device number in '/dev/ttyACM\{\}'")
    parser.add_argument("--file", help="Output file name '\{\}.csv'")

    args = parser.parse_args()

    if args.device is not None:
        device_number = args.device
    if args.file is not None:
        file_name = args.file

    signal.signal(signal.SIGINT, handler)
    main()



