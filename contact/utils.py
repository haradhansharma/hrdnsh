from django.core.mail.message import (
    DEFAULT_ATTACHMENT_MIME_TYPE,
    BadHeaderError,
    EmailMessage,
    EmailMultiAlternatives,
    SafeMIMEMultipart,
    SafeMIMEText,
    forbid_multi_line_headers,
    make_msgid,
)
from django.core.mail import get_connection

def send_mail(
    subject,
    message,
    from_email,
    recipient_list,
    cc=None,
    bcc=None,    
    reply_to=None,
    fail_silently=False,
    auth_user=None,
    auth_password=None,
    connection=None,
    html_message=None,
):
    
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )

    mail = EmailMultiAlternatives(
        subject,
        message,
        from_email,
        recipient_list,
        cc=cc,
        bcc=bcc,        
        reply_to=reply_to,
        connection=connection,
    )

    if html_message:
        mail.attach_alternative(html_message, "text/html")

    return mail.send()

