import os
import csv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email, first_name):
    message = Mail(
        from_email='noah@ntslogistics.com',
        to_emails=to_email,
        subject='Is there anything else I could help you with?',
        html_content=(
            f'Hey {first_name},<br /><br />'
            'I wanted to make sure you still had my contact in case you needed a transport rate.<br />'
            'Do you have any upcoming transports or anything you\'re planning purchase that you need a shipping rate for?</strong><br /><br />'
            'Best regards,<br /><br />'
    'Noah<br />'
    '954-495-8184<br />'
    'noah@nationwidetransportservices.com<br /><br />'
    '<img src="https://cdn-ikpnonn.nitrocdn.com/waDtbKwbaGRAyvseWdfAzZVchgcglzdg/assets/images/source/rev-834ffae/ntslogistics.com/wp-content/uploads/2019/11/NTS-logo.svg" alt="Company Logo" style="width:100px; height:auto;">'
    '<img src="https://www.heavyhaulers.com/images/hh-label-icons/hh-verticle-logo-final.png" alt="Company Logo style="height:225px; width:auto;"">'
        ))  
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")
        return None

def main():
    with open('test.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row['email']
            first_name = row['first_name']
            status_code = send_email(email, first_name)
            if status_code:
                print(f"Email sent to {email} (Status code: {status_code})")
            else:
                print(f"Failed to send email to {email}")

if __name__ == "__main__":
    main()