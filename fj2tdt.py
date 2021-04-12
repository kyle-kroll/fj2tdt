"""
    Title: FlowJo 2 TDT
    About: Script that takes in one or more FlowJo CSV files from boolean gating and produces
           a single tab-delimited text file that can be fed into Pestle for SPICE visualizations
    Author: Kyle Kroll
    Date: 2021-04-12
"""

# Libraries required
import pandas as pd
import argparse
import os
import re

# Initiate the parser and add arguments
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Enable verbose output", action="store_true")
parser.add_argument("-i", "--input", help="Input file(s)", required=True)
parser.add_argument("-s", "--separator", help="File separator: comma or tab", required=True)
parser.add_argument("-o", "--output", help="Output file", required=True)
parser.add_argument("-S", "--spice", help="Format for SPICE?", action="store_true")

# Read arguments from the command line
args = parser.parse_args()

# Parse arguments for required information
print("Parsing arguments ...") if args.verbose else None
input_files = args.input
output_file = args.output
file_separator = "," if args.separator == "comma" else "\t"

# Check input if it is a directory
if os.path.isdir(input_files):
    print("Placeholder. Please supply single files only for now.")
else:
    try:
        print("Reading input file ...") if args.verbose else None
        input_data = pd.read_csv(input_files, sep=file_separator)
        column_names = input_data.columns.tolist()
        column_names[0] = "File"
        input_data.columns = column_names
    except OSError as e:
        print("Error reading file. Please check that you entered the filename correctly.")
        print(e)

# Parse dataframe to fix column names
format_header = []
variables = ""
print("Fixing column names ...") if args.verbose else None
i = 1
num = len(input_data.columns.tolist())
for x in input_data.columns.tolist():
    if "/" in x:
        m = re.search(r"([A-Za-z0-9]+[+-]){2,5} \|", x)
        column_val = m.group(0)
        format_header.append(column_val.replace(r" |", ""))
        variables = column_val.replace(r" |", "")
    else:
        format_header.append(x)
    print(f"Finished column {i} / {num}") if args.verbose else None
    i = i + 1

# Set new column header
input_data.columns = format_header


# Define function for parsing data to SPICE format
# See https://niaid.github.io/spice/help/delimitedformat for format specification
def format_spice(data):
    return data


# Iterate through data frame to create SPICE formatted file
if args.spice:
    output_data = format_spice(input_data)
else:
    output_data = input_data
