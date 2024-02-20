from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jwt
from datetime import datetime, timezone, timedelta
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse


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
        html_content = "<html><body>"
        html_content += "<h1>Confirm Email at <em>Techies Corner</em></h2>"
        html_content = "<h2><em>Click below to confirm your email</em></h2>"
        html_content += f"<a href='{url}'>Confirm Email</a>"
        html_content += "<p>Do not reply to this email<p>"
        html_content += "</body></html>"
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
