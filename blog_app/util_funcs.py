from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jwt
from datetime import datetime, timezone, timedelta
from django.urls import reverse
from bs4 import BeautifulSoup
import requests
from .forms import NewsForm


SECRET_KEY = 'django-insecure-c)4*)!$+j-u-$7kp@s9)amqzu2@9=oj6*9&5k0fgf993imzijf'
ALGORITHM = 'HS256'
EMAIL_USER = 'taskhub2023@gmail.com'
EMAIL_PASSWORD = 'xmyp fkpl evos iltv'
EMAIL_HOST = 'smtp.gmail.com'
HOST = '127.0.0.1:8000'


class UtilClass:

    def encode_id(self, user_id):
        """encode a user id using jwt"""

        exp = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
        payload = {'user_id': str(user_id),
                   'exp': exp}
        secret_key = SECRET_KEY
        algorithm = ALGORITHM
        encoded_jwt = jwt.encode(payload, secret_key, algorithm=algorithm)
        return encoded_jwt
    
    def decode(self, encoded_jwt):
        """decode an encoded jwt"""

        decoded = None
        error = None
        try:
            decoded = jwt.decode(encoded_jwt,
                                 SECRET_KEY,
                                 algorithms=ALGORITHM)
            if decoded:
                decoded = decoded.get('user_id')
        except jwt.ExpiredSignatureError as e:
            error = e
        finally:
            return {'user_id': decoded, 'error': error}

    def confirm_email(self, request, user_id, user_email):
        """send an email confirmation to user email"""

        encoded_jwt = self.encode_id(user_id)
        url = request.build_absolute_uri(reverse('blog_app:confirm_email',
                                                 kwargs={'encoded': encoded_jwt}))
        html_content = f"""
                <html>
                    <body>
                        <div style='margin: 5px; background-color: #eae7e7;'>
                            
                            <h1 style='color: rgb(66, 151, 236); margin: 5px; text-align: center;'>Techies Corner</h1>
                            <h2 style='color: rgb(66, 151, 236); margin: 5px; text-align: center;'>Go ahead and confirm your email<h2>
                            <p><em style='font-size: 15px; text-align: center;'>With Techies Corner, you are always up to date with the latests in the tech community.
                            Your account creation is almost complete. By confirming your email address, you let
                            us know you are the rightful owner to this account</em></p>
                            <div style='background-color: #027af9;
                            display: flex; justify-contents: center;
                            align-items: center; width: fit-content;
                            height: auto; padding: 10px; border-radius: 10px;'>
                            <a style='color: white; text-align: center;' href='{url}'>Confirm Your Email Address</a>
                            </div>
                            <p style='font-weight: lighter; font-size: 12px;'>Do not reply to this email<p>
                        </div>
                    </body>
                </html>
                """
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_USER
        msg['To'] = user_email
        msg['Subject'] = 'Confirm Your Techies Corner Email'
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        with SMTP(EMAIL_HOST) as connection:
            connection.starttls()
            connection.login(EMAIL_USER, EMAIL_PASSWORD)
            connection.sendmail(EMAIL_USER, user_email, msg.as_string())
    
    def forgot_password(self, request, user_id, user_email):
        """send a forgot password email"""

        encoded_jwt = self.encode_id(user_id)
        url = request.build_absolute_uri(reverse('blog_app:reset_password',
                                                 kwargs={'encoded': encoded_jwt}))
        html_content = f"""
                <html>
                    <body>
                        <div style='margin: 5px; padding: 5px;'>
                            <h1 style='color: rgb(66, 151, 236); margin: 5px; text-align: center;'>Techies Corner</h1>
                            <h2 style='color: rgb(66, 151, 236); margin: 5px; text-align: center;'>Reset Your Techies Corner Password</h2>
                            <p><em style='font-size: 15px; text-align: center;'>This email was sent as a result of password rest request
                            on your account. If you did not request this. Log on to your techies corner account to update your password and further secure your acount</em></p>
                            <div style='background-color: #027af9;
                            display: flex; justify-contents: center;
                            align-items: center; width: fit-content;
                            height: auto; padding: 10px; border-radius: 10px;'>
                            <a style='color: white; text-align: center;' href='{url}'>Reset your password</a>
                            </div>
                            <p style='font-weight: lighter; font-size: 12px;'>Do not reply to this email<p>
                        </div>
                    </body>
                </html>
                """
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_USER
        msg['To'] = user_email
        msg['Subject'] = 'Reset Your Techies Corner Password'
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        with SMTP(EMAIL_HOST) as connection:
            connection.starttls()
            connection.login(EMAIL_USER, EMAIL_PASSWORD)
            connection.sendmail(EMAIL_USER, user_email, msg.as_string())


class NewsScraper:

    def get_news(self):
        """scrape techmeme for news"""

        try:
            response = requests.get('https://techmeme.com/')
        except requests.exceptions.ConnectionError:
            print("Network Error")
            response = None
        result = {}
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.select(selector='div#topcol1 div.clus > .itc1 strong .ourh')
            summaries = soup.select(selector='div#topcol1 div.clus > .itc1 div .ii')
            links = [i['href'] for i in titles]
            titles = [i.get_text().split('\n')[0] for i in titles]
            summaries = [i.get_text() for i in summaries]
            result = {
                'titles': titles,
                'links': links,
                'summaries': summaries
            }
        return result
    
    def update_news_db(self):
        """update the news database"""

        data = self.get_news()
        links = data.get('links')
        titles = data.get('titles')
        summaries = data.get('summaries')

        if links and titles and summaries:
            length = len(titles)
            for i in range(length):
                try:
                    form = NewsForm({'title': titles[i],
                                     'summary': summaries[i],
                                     'link': links[i]})
                except IndexError:
                    break
                else:
                    if form.is_valid():
                        form.save()
