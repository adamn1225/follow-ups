import os
import csv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ... keep the send_email function as is ...

def main():
    with open('test.csv', 'r') as csvfile:
        reader = list(csv.DictReader(csvfile))
        fieldnames = reader[0].keys()  # Get the column names
    
    # Reverse the list to start from the bottom
    reader.reverse()
    # Take only the first 10 entries
    recipients = reader[:10]
    # The remaining entries
    remaining = reader[10:]

    for row in recipients:
        email = row['email']
        first_name = row['first_name']
        status_code = send_email(email, first_name)
        if status_code:
            print(f"Email sent to {email} (Status code: {status_code})")
        else:
            print(f"Failed to send email to {email}")
    
    # Write the remaining entries back to the CSV
    with open('test.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reversed(remaining))  # Reverse again to maintain original order

    print(f"Processed 10 entries. {len(remaining)} entries remaining in the CSV.")

if __name__ == "__main__":
    main()