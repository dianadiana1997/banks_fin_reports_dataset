import csv
import argparse
import glob
import os.path


def merge_csv(csv_dir, out_path):
    global_header = True
    with open(out_path, 'w') as output:
        for file in glob.glob(os.path.join(csv_dir, "*.csv")):
            header = True
            with open(file, 'r') as r:
                for line in r.readlines():
                    if header and not global_header:
                        header = False
                        continue
                    output.write(line)
                    global_header = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Соединение нескольких датасетов в директории в один')
    parser.add_argument('-d', '--dir', type=str,
                        help='Путь до директории с csv файлами', required=False)
    parser.add_argument('-o', '--out', type=str,
                        help='Путь для сохранения результирующего датасета', required=False)
    args = parser.parse_args()

    merge_csv(args.dir, args.out)
