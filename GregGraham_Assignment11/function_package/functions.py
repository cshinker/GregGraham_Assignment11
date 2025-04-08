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
import os


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

    def remove_duplicates(self, data):
        """
        Removes duplicate rows from a list of dictionaries while ignoring the first column.
        It checks for duplicates based on all columns except the first one.

        Args:
            data (list): A list of dictionaries, where each dictionary represents a
                         row from a CSV file.

        Returns:
            list: A new list of dictionaries with duplicate rows removed, ignoring the first column.
        """
        if not data:
            return []

        # Get the column headers
        headers = list(data[0].keys())

        # Create a set to track the seen rows (ignoring the first column)
        seen = set()
        unique_data = []

        # Loop through each row
        for row in data:
            # Create a tuple of the row excluding the first column (the first column's key)
            row_values_excluding_first_column = tuple((key, value) for key, value in row.items() if key != headers[0])

            # If this row (ignoring the first column) hasn't been seen yet, add it to unique_data
            if row_values_excluding_first_column not in seen:
                unique_data.append(row)
                seen.add(row_values_excluding_first_column)

        return unique_data

    def remove_pepsi(self, data, phrase="Pepsi"):
        """
        Deletes the fuel type if the value in the 6th column corresponds to "Pepsi" and writes those rows to 'dataAnomalies.csv'.

        Args:
            data (list): A list of dictionaries, where each dictionary represents a row.
            phrase (str): The phrase to search for (default is "Pepsi").

        Returns:
            list: The updated list of dictionaries where fuel type is removed if it contains "Pepsi".
        """
        if not data:
            return []

        # Create 'Data' folder if it doesn't exist
        os.makedirs('Data', exist_ok=True)

        # Prepare the data for anomalies and valid rows
        anomaly_data = []
        valid_data = []

        # Get the headers (column names)
        headers = list(data[0].keys())

        # Loop through each row and check for the anomaly
        for row in data:
            if len(headers) >= 6:  # Ensure there are at least 6 columns
                # Get the value of the 6th column (index 5)
                if phrase in row[headers[5]]:  # Check if 'Pepsi' is in the 6th column
                    # Save this row as an anomaly
                    anomaly_data.append(row)
                    # Remove the 6th column from the row (fuel type)
                    del row[headers[5]]
            valid_data.append(row)

        # Write anomalies to a new CSV file (dataAnomalies.csv)
        if anomaly_data:
            with open('Data/dataAnomalies.csv', 'w', newline='', encoding='utf-8') as anomaly_file:
                writer = csv.DictWriter(anomaly_file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(anomaly_data)
        else:
            print("No anomalies found to write.")

        # Return the cleaned data
        return valid_data