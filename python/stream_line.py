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
    lines = ["CHAN_2,CHAN_26,CHAN_80,ORI,GRID"]
    grid = [8, 1, 15, 19]
    ori_list = [0]
    for i, line in enumerate(in_file.readlines()):
        # print(ori_list[i%4])
        # print(",{},{}".format(ori_list[i%4], int(i/4)))
        lines.append(line.strip() + ",{},{}".format(ori_list[i%1], grid[i]))
    in_file.close()
    out_file = open('../data/' + out_file + '.csv', "w")
    out_file.write("\n".join(lines))
    out_file.close()