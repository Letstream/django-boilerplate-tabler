from django.template.loader import get_template
from django.core.mail.backends.smtp import EmailBackend
from django.core import mail

from apps.core.utils import getOption

def send_mail(email):

    try:
        # plaintext = get_template("%s/template.txt" % template).render(context)
        # html = get_template("%s/template.html" % template).render(context)

        con = mail.get_connection(
            host = getOption("smtp_server"),
            port = getOption("smtp_port"),
            username = getOption("smtp_user"),
            password = getOption("smtp_pass"),
            use_tls = True
        )

        msg = mail.EmailMultiAlternatives(
            subject = email.subject,
            body = email.plain_text,
            from_email = email.from_email,
            to = [email.to_email],
            connection = con
        )
        
        msg.attach_alternative(email.html_text, "text/html")
        msg.send()
        
        return True
    except Exception as e:
        raise