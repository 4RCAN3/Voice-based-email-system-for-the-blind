import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from bs4 import BeautifulSoup
import smtplib, socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mails():
    
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def SendMail(self, receiverMail, Subject, content):
        sender = self.username
        password = self.password

        while True:
            try:
                message = MIMEMultipart()

                message['From'] = sender
                message['To'] = receiverMail
                message['Subject'] = Subject

                #The body and the attachments for the mail
                message.attach(MIMEText(content, 'plain'))

                #Create SMTP session for sending the mail
                session = smtplib.SMTP('smtp.office365.com', 587) #use gmail with port
                session.starttls() #enable security

                session.login(sender, password) #login with mail_id and password
                text = message.as_string()
                session.sendmail(sender, receiverMail, text)
                session.quit()
                print('Mail Sent')
                
                break
            except socket.error as e:
                print(e)
                pass
        


    def ReadMail(self):
        
        """
        Read the latest mail from the inbox
        """
        
        def clean(html):
            soup = BeautifulSoup(html, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text

        # account credentials
        username = self.username
        password = self.password

        imap_server = "outlook.office365.com"
        imap = imaplib.IMAP4_SSL(imap_server, port=993)

        # authenticate
        imap.login(username, password)
        status, messages = imap.select("INBOX")
        messages = int(messages[0])
        N = 1

        for i in range(messages, messages-N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")

            for response in msg:

                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)

                    # if the email message is multipart

                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                                return (subject, From, clean(body))
                            except:
                                pass
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        return (subject, From, clean(body))
                    