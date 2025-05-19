import argparse
import subprocess
from datetime import datetime



def argument_parser():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("file", help="Input file path")
    parser.add_argument("site", help="Site type")
    return parser.parse_args()

def main():
    args = argument_parser()
    file = args.file
    site = args.site
    command = f"py main.py -f {file} -s {site} && py validation.py output/{site.title()}_{datetime.now().date()}.json && py check_new.py output/{site.title()}_{datetime.now().date()}_validated.json"
    # command = f"rm -rf logs/ && py main.py -f {file} -s {site} && py validation.py output/{site.title()}_{datetime.now().date()}.json && py check_new.py output/{site.title()}_{datetime.now().date()}_validated.json"
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()
