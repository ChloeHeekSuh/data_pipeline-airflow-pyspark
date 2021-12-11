import argparse
import ast  # converts json file into dictionary
from pyspark.sql import SparkSession
from pipeline_utils.package import SparkParams


# It will take care of the command line in json blob
# dictionary 로 넣고, 저장하면 나중에 콘솔에서 키워드를 사용가능!
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--params", required=True, help="Spark input parameter {'input_path': ...., 'name': 'demo', 'file_type': txt.....}")
# The parse_args() method actually returns some data from the options specified like '-p', 'i', etc.
args = parser.parse_args()

print("args" + str(args))

# It will take the input parameter string of json blob into a dictionary
def parse_command_line(args):
    # for line in open(args):
    #     yield ast.literal_eval(line)
    return ast.literal_eval(args)


def spark_init(parser_name):
    ss = SparkSession \
        .builder \
        .appName(parser_name) \
        .getOrCreate()
    ss.sparkContext.setLogLevel1("ERROR")
    return ss


# we are getting a key value pair as dict in python
parse_command_line = parse_command_line(args)
params = SparkParams(parse_command_line)
spark = spark_init(params)

if __name__ == "__main__":
    print("Executing script via pyspark")