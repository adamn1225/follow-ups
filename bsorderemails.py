import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import csv

def scrape_order_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'tblOrders'})
    if not table:
        return []

    unique_entries = set()  # Use a set to store unique entries
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 5:  # Name and email are in the 5th column
            info_cell = cells[4]
            name = info_cell.contents[0].strip().split()[0]  # Get only the first name
            email_link = info_cell.find('a', class_='aUnderline')
            if email_link:
                email = email_link.text.strip()
                unique_entries.add((name, email))  # Add tuple to set

    return [{'first_name': name, 'email': email} for name, email in unique_entries]

# Add these lines at the end of the file
if __name__ == "__main__":
    # Read the HTML file
    with open('pastorders.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Call the function with the file content
    orders = scrape_order_table(html_content)
    
    # Write orders to CSV
    with open('unique_orders.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['first_name', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for order in orders:
            writer.writerow(order)
    
    print(f"Found {len(orders)} unique emails. Data written to unique_orders.csv")