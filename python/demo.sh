#!/bin/bash
python csv_parser.py --in_file=0-0 --out_file=0-0-parse
python csv_parser.py --in_file=0-4 --out_file=0-4-parse
python csv_parser.py --in_file=4-0 --out_file=4-0-parse
python csv_parser.py --in_file=4-4 --out_file=4-4-parse
python stream_line.py --in_file=0-0-parse --out_file=0-0-cleaned
python stream_line.py --in_file=0-4-parse --out_file=0-4-cleaned
python stream_line.py --in_file=4-0-parse --out_file=4-0-cleaned
python stream_line.py --in_file=4-4-parse --out_file=4-4-cleaned
python concat_data.py -f 0-0-cleaned -f 0-4-cleaned -f 4-0-cleaned -f 4-4-cleaned -o final
python model_build.py -d final -t final