import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(subject, message, from_email, to_email, password, file_path):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with open(file_path, 'rb') as f:

        attachment = MIMEApplication(f.read(), _subtype='docx')
        attachment.add_header('Content-Disposition', 'attachment', filename='Письмо об участии в соревновании.docx')
        msg.attach(attachment)

    try:
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print('Message sent')
    except Exception as e:
        print(str(e))

