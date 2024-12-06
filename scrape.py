import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Fetch the webpage content
url = "https://edgar.jrc.ec.europa.eu/report_2024"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Step 2: Locate the table
table = soup.find('table')  # Locate the first table, adjust if necessary

# Step 3: Extract column names and units
header_rows = table.find('thead').find_all('tr')
columns = [header.text.strip() for header in header_rows[0].find_all('th')]
units = [unit.text.strip() for unit in header_rows[1].find_all('th')]

# Combine column names and units
columns_with_units = [f"{col} ({unit})" for col, unit in zip(columns, units)]

# Step 4: Extract the table data
rows = table.find('tbody').find_all('tr')
data = []
for row in rows:
    cells = row.find_all('td')
    data.append([cell.text.strip() for cell in cells])

# Step 5: Create DataFrame and save to CSV
df = pd.DataFrame(data, columns=columns_with_units)
df.to_csv('edgar_data.csv', index=False)

# Print the first few rows to confirm
print(df.head())