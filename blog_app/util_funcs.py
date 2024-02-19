from django.core.mail import EmailMultiAlternatives
import jwt
from datetime import datetime, timezone, timedelta
from django.urls import reverse


SECRET_KEY = 'django-insecure-c)4*)!$+j-u-$7kp@s9)amqzu2@9=oj6*9&5k0fgf993imzijf'
ALGORITHM = 'HS256'


class UtilClass:

    def encode_id(self, user_id):
        """encode a user id using jwt"""

        exp = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
        payload = {'user_id': user_id,
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
        except jwt.ExpiredSignatureError as e:
            error = e
        finally:
            return {'decoded': decoded, 'error': error}

    def confirm_email(self, user_id, user_email):
        """send an email confirmation to user email"""

        encoded_jwt = self.encode_id(user_id)
        url = reverse('blog_app:confirm_email', args=[encoded_jwt])
        subject = "Confirm Email"
        text_content = "Please click the following link to"
        text_content += f" confirm your email with Techies Corner {url}"
        html_content = "<h1>Confirm Email at <em>Techies Corner</em></h2>"
        html_content = "<h2><em>Click below to confirm your email</em></h2>"
        html_content += f"<a href='{url}'>Confirm Email</a>"
        msg = EmailMultiAlternatives(subject, text_content,
                                     "taskhub2023@gmail.com",
                                     [user_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
