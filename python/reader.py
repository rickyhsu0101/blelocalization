import sys
import signal
import serial


file_name = "collected.csv"
data = []
def write_file():
    with open("../data/collected.csv", "w") as f:
        for line in data:
            f.write(line + "\n")
        f.close()

def handler(signum, frame):
    write_file()
    exit(0)

def main(v):
    ser = serial.Serial('/dev/ttyACM{}'.format(v))
    while(1):
        line = ser.readline()
        data.append(line)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        file_name = sys.argv[1]
    signal.signal(signal.SIGINT, handler)
    main()



