import argparse
from distutils import util

from data_processing_job import DataProcessingJob

parser = argparse.ArgumentParser(description="Enter columns to include and whether to add background color on rows")

parser.add_argument("-k", "--keys", type=str, nargs="+", required=True)
parser.add_argument("-c", "--colored", type=lambda x: bool(util.strtobool(x)), default=True)
args = parser.parse_args()

if __name__ == "__main__":
    job = DataProcessingJob(args.keys, args.colored)
    job.run()
