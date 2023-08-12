import csv
import os

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the CSV file
csv_file_path = os.path.join(script_directory, 'category.csv')

with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)