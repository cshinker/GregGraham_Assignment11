# File Name: main.py
# Student Name: Cam Shinker, Luke elmore
# email: shinkecj@mail.uc.edu, elmorels@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date: 4/17/2025
# Course #/Section: IS 4010-002
# Semester/Year: Spring 2025
# Brief Description of the assignment: Clean some messy CSV data

# Brief Description of what this module does: Contains the entry point code for the assignment
# Citations: 

# Anything else that's relevant:

from function_package.functions import *
if __name__ == "__main__":
    csv = csv_Functions()
    data_list = csv.read_csv("Data/fuelPurchaseData.csv")
    rounded_data = csv.round_price(data_list)

    duplicate_data = csv.remove_duplicates(rounded_data)

    pepsi_removed = csv.remove_pepsi(duplicate_data)

    csv.check_fraud(pepsi_removed)
    
