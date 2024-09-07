from bs4 import BeautifulSoup
import csv


def scrape_order_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'tblQuote'})
    if not table:
        return []
    
    orders = []
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 4:  # Ensure we have enough cells
            info_cell = cells[3]  # The 4th column contains name and email
            name_parts = info_cell.contents[0].strip().split()
            first_name = name_parts[0] if name_parts else ""
            email_link = info_cell.find('a', class_='aUnderline')
            if email_link:
                email = email_link.text.strip()
                orders.append({'email': email, 'first_name': first_name})
    
    return orders

if __name__ == "__main__":
    with open('pastorders.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    orders = scrape_order_table(html_content)
    
    with open('orders_with_names.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['email', 'first_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for order in orders:
            writer.writerow(order)
    
    print(f"Found {len(orders)} orders. Data written to orders_with_names.csv")