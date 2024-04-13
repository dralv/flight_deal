import smtplib
import email.message
import os
class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def send_email(self,price,origin,destination,date_to,data_from):
        corpo_email = f""""
        <p>Only {price} to fly from {origin} to {destination}, from {date_to} to {data_from}
        """
        msg = email.message.Message()
        msg['Subject'] = "Low Price Alert"
        msg['From'] = "devalvinho7@gmail.com"
        msg['To'] = "devalvinho7@gmail.com"
        password = os.environ['EMAIL_APP_PASSWORD']
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=msg['From'],password=password)
            connection.sendmail(msg['From'],msg['To'],msg.as_string().encode('utf-8'))