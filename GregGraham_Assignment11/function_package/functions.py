# File Name: functions.py
# Student Name: Cam Shinker, Luke elmore
# email: shinkecj@mail.uc.edu, elmorels@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date: 4/17/2025
# Course #/Section: IS 4010-002
# Semester/Year: Spring 2025
# Brief Description of the assignment: Clean some messy CSV data

# Brief Description of what this module does: Contains a class with functions to perform the assignment
# Citations: 

# Anything else that's relevant:

import csv

class csv_Functions():
    def read_csv(self, file_path):
        """
        Reads a CSV file that contains a column header row and returns the data
        as a list of dictionaries. Each dictionary represents a row, with keys
        being the column headers.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            list: A list of dictionaries, where each dictionary represents a row
                  and keys are the column headers. Returns an empty list if the
                  file is empty or an error occurs.
        """
        data = []
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
        return data

    def round_price(self, data):
        """
        Takes a list of dictionaries and formats the values in the third column
        (if it exists and is numeric) to exactly two decimal places, even if
        the original number has fewer.

        Args:
            data (list): A list of dictionaries, where each dictionary represents a
                         row from a CSV file with a header.

        Returns:
            list: The same list of dictionaries, but with the values in the third
                  column formatted to exactly two decimal places (if applicable).
        """
        if not data:
            return []

        if len(data[0]) < 3:
            print("Warning: The data dictionaries have fewer than three columns. No formatting performed.")
            return data

        headers = list(data[0].keys())
        third_column_header = headers[2]  # Assuming 0-based indexing

        for row in data:
            try:
                value = float(row[third_column_header])
                row[third_column_header] = "{:.2f}".format(value)
            except (ValueError, KeyError):
                # Handle cases where the third column value is not a number
                # or if the header somehow disappeared
                pass  # Keep the original value if formatting fails
        return data