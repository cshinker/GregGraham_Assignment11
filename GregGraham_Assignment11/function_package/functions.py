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
import requests
import re


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
        Deletes the entire row if the value in the 6th column corresponds to "Pepsi"
        and writes those rows to 'dataAnomalies.csv'.

        Args:
            data (list): A list of dictionaries, where each dictionary represents a row.
            phrase (str): The phrase to search for (default is "Pepsi").

        Returns:
            list: The updated list of dictionaries with rows containing "Pepsi" in the
                  6th column removed.
        """
        if not data:
            return []

        # Create 'Data' folder if it doesn't exist
        os.makedirs('Data', exist_ok=True)

        # Prepare the data for anomalies and valid rows
        anomaly_data = []
        valid_data = []

        # Get the headers (column names) from the first row
        if data:
            headers = list(data[0].keys())
        else:
            headers = []

        # Loop through each row and check for the anomaly
        for row in data:
            if len(headers) >= 6:  # Ensure there are at least 6 columns
                # Get the value of the 6th column (index 5)
                if phrase in row.get(headers[5], ''):  # Check if 'Pepsi' is in the 6th column (handle potential missing key)
                    # Save the entire row as an anomaly
                    anomaly_data.append(row)
                else:
                    # Keep the row in the valid data
                    valid_data.append(row)
            else:
                # If there are fewer than 6 columns, consider it valid
                valid_data.append(row)

        # Write anomalies to a new CSV file (dataAnomalies.csv)
        if anomaly_data and headers:
            with open('Data/dataAnomalies.csv', 'w', newline='', encoding='utf-8') as anomaly_file:
                writer = csv.DictWriter(anomaly_file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(anomaly_data)
        elif anomaly_data:
            print("Warning: No headers found to write the anomaly file.")
        else:
            print("No anomalies found to write.")

        # Return the cleaned data
        return valid_data

    def check_fraud(self, data):
        """
        Checks if there are multiple rows in the given data where the values
        in the 5th column (index 4) and the 9th column (index 8) are equal,
        and writes *all* such rows to 'possiblefraud.csv' in the 'Data' folder.

        Args:
            data (list): A list of dictionaries, where each dictionary represents a row.

        Returns:
            bool: True if duplicate rows were found and written, False otherwise.
        """
        if not data or len(data) < 2:
            print("Not enough rows to check for duplicates.")
            return False

        potential_fraud_rows = []
        pair_counts = {}
        headers = list(data[0].keys()) if data else []

        if len(headers) < 9:
            print("Warning: The data has fewer than 9 columns. Cannot reliably check column 9.")
            return False

        column5_name = headers[4]
        column9_name = headers[8]

        # First pass: Count occurrences of each (column5, column9) pair
        for row in data:
            value_column5 = row.get(column5_name)
            value_column9 = row.get(column9_name)

            if value_column5 is not None and value_column9 is not None:
                pair = (value_column5, value_column9)
                pair_counts[pair] = pair_counts.get(pair, 0) + 1

        # Second pass: Identify rows with pairs that appeared more than once
        for row in data:
            value_column5 = row.get(column5_name)
            value_column9 = row.get(column9_name)

            if value_column5 is not None and value_column9 is not None:
                pair = (value_column5, value_column9)
                if pair_counts[pair] > 1:
                    potential_fraud_rows.append(row)

        # Create 'Data' folder if it doesn't exist
        os.makedirs('Data', exist_ok=True)

        # Write potential fraud rows to 'possiblefraud.csv'
        if potential_fraud_rows and headers:
            with open('Data/possiblefraud.csv', 'w', newline='', encoding='utf-8') as fraud_file:
                writer = csv.DictWriter(fraud_file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(potential_fraud_rows)
            print(f"Found {len(potential_fraud_rows)} rows with matching values in columns 5 and 9. "
                  f"These rows have been written to 'Data/possiblefraud.csv'.")
            return True
        elif potential_fraud_rows:
            print("Warning: No headers found to write the possible fraud file.")
            return True
        else:
            print("No rows found with matching values in columns 5 and 9 across multiple rows.")
            return False



    def fill_zip_codes(self, data, api_key):
        """
        Appends ZIP codes to full addresses (in the 4th column) for the first 5 rows 
        that are missing ZIP codes. Uses city/state via the Zipcodebase API and 
        writes the full cleaned dataset to Data/cleanedData.csv.

        Args:
            data (list): List of dictionaries representing rows.
            api_key (str): Zipcodebase API key.

        Returns:
            list: Updated data with ZIPs added to the first 5 missing.
        """
        if not data:
            return []
        # Comment out
        headers = list(data[0].keys())
        if len(headers) < 4:
            return data

        address_col = headers[3]
        zip_cache = {}
        filled_count = 0
        max_to_fill = 5

        for row in data:
            if filled_count >= max_to_fill:
                break

            full_address = row.get(address_col, '').strip()

            # Skip if ZIP is already present
            if re.search(r'\b\d{5}(?:-\d{4})?\b', full_address):
                continue

            parts = full_address.split(',')
            if len(parts) >= 2:
                city = parts[-2].strip()
                state = parts[-1].strip()[:2].upper()

                if city and state:
                    key = f"{city},{state}"
                    if key in zip_cache:
                        zip_code = zip_cache[key]
                        row[address_col] = f"{full_address} {zip_code}"
                        filled_count += 1
                        continue

                    try:
                        #url = f"https://app.zipcodebase.com/api/v1/code/city?city={city}&state={state}"
                        url = "https://app.zipcodebase.com/api/v1/code/city?apikey="+api_key+"&city="+city+"&country=us"
                        response = requests.get(url)
                        if response.status_code == 200:
                            result = response.json()
                            zip_codes = result.get("results", {}).get(key, [])
                            if zip_codes:
                                zip_code = zip_codes[0]
                                zip_cache[key] = zip_code
                                row[address_col] = f"{full_address} {zip_code}"
                                filled_count += 1
                    except Exception:
                        pass
        # Comment out
        # Save the result to 'Data/cleanedData.csv'
        os.makedirs('Data', exist_ok=True)
        with open('Data/cleanedData.csv', 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

        return data