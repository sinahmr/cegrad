from django.core.mail import EmailMessage
from django.template.loader import get_template


def send_mail(to, context, email_template_name):
    title = 'سامانه‌ی فارغ‌التحصیلی CE93'  # TODO
    message = get_template('main/email/%s.html' % email_template_name).render(context)  # TODO template text
    msg = EmailMessage(title, message, to=[to], from_email='cegrad93@gmail.com')
    msg.content_subtype = 'html'
    msg.send()
