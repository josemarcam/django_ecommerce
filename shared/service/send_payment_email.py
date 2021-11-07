from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings


def send_mail(instance,template:str,subject:str):
        recibient_email = instance.email
        html_content = render_to_string(template,
        {
            "order":instance.order,
            "item_description":instance.order.get_description,
            "total_price":instance.order.get_total_price,
            "customer_name":instance.order.name
        })
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject = subject,
            body = text_content,
            from_email = settings.DEFAULT_FROM_EMAIL,
            to = [recibient_email],
        )
        email.attach_alternative(html_content,"text/html")
        email.send(not settings.DEBUG)