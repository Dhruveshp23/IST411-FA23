import smtplib
from email.mime.text import MIMEText

# Define the sender and recipient email addresses
fromAddress = 'drp5554@psu.edu'
toAddress = 'drp5554@psu.edu'

# Set the email subject and message content
subject = 'Email Solo Lab with Python'
message_content = 'It worked!'

# Create a MIMEText object for the email message
msg = MIMEText(message_content)
msg['Subject'] = subject
msg['From'] = fromAddress
msg['To'] = toAddress

try:
    # Create an SMTP_SSL instance using the PSU email server and port 465
    s = smtplib.SMTP_SSL('authsmtp.psu.edu', 465)

    # Send the email
    s.sendmail(fromAddress, [toAddress], msg.as_string())
    print("Email sent successfully.")

except smtplib.SMTPException as e:
    print("Error: ", str(e))

finally:
    # Ensure that the SMTP connection is closed, whether an error occurred or not
    s.quit()
