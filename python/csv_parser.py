import csv
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_file", help = "input filename of csv file")
    parser.add_argument("--out_file", help="output filename of csv file")
    args = parser.parse_args()
    in_file = ""
    out_file = ""
    if args.in_file is not None:
        in_file = args.in_file
    if args.out_file is not None:
        out_file = args.out_file

    in_file = open('../data/' + in_file + '.csv', "r")
    out_file = open('../data/' + out_file + '.csv', "w")
    csvread = csv.reader(in_file)
    csvwrite = csv.writer(out_file)

    csvreader = csv.reader(x.replace("\0", '') for x in in_file)
    
    for row in csvreader:
        if len(row) != 3:
            continue
        csvwrite.writerow(row)
    