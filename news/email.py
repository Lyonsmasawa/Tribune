from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(name, receiver):
    #creating subject and sender
    subject = 'Welcome to the MoringaTribune NewsLetter'
    sender = 'renderwes@gmail.com'

    #passing in the context variables
    text_context = render_to_string('email/newsemail.txt', {"name":name})
    html_context = render_to_string('email/newsemail.html', {"name":name})

    msg = EmailMultiAlternatives(subject, text_context, sender, [receiver])
    msg.attach_alternative(html_context, 'text/html')
    msg.send()

