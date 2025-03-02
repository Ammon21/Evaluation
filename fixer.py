import pandas as pd
import os

# List of your 9 Excel file paths
xlsx_files = ['9a.xlsx', '9b.xlsx', '9c.xlsx', '11a.xlsx', '11b.xlsx','11c.xlsx',  '12a.xlsx', '12b.xlsx','12c.xlsx']

#'5a.xlsx', '5b.xlsx', '5c.xlsx' #'5a.xlsx', '5b.xlsx', '5c.xlsx'
#,'7a.xlsx', '7b.xlsx', '7c.xlsx','8a.xlsx', '8b.xlsx','8c.xlsx'

# Convert all .xlsx files to .csv
for file in xlsx_files:
    # Read the Excel file
    data = pd.read_excel(file)
    
    # Save the data as a .csv file
    csv_filename = os.path.splitext(file)[0] + '.csv'
    data.to_csv(csv_filename, index=False)
    print(f"Converted {file} to {csv_filename}")

# Now merge all CSV files
csv_files = [os.path.splitext(file)[0] + '.csv' for file in xlsx_files]  # Create list of CSV file names

# Read all CSV files and concatenate them into one dataframe
merged_data = pd.concat([pd.read_csv(csv_file) for csv_file in csv_files], ignore_index=True)

# Save the merged data to a new CSV file
merged_data.to_csv('merged_data.csv', index=False, encoding='utf-8')

# Print confirmation
print("All files have been merged into 'merged_data.csv'")
