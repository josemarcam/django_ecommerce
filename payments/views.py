# TODO
# Executar envio de email por celery

import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.functional import cached_property
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from shared.service.send_payment_email import send_mail

from orders.models import Order

from .forms import PaymentForm, UpdatePaymentForm
from .models import Payment


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm

    @cached_property
    def order(self):
        order_id = self.request.session.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        return order

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["order"] = self.order
        return form_kwargs

    def form_valid(self, form):
        form.save()
        redirect_url = "payments:failure"
        status = form.instance.mercado_pago_status


        if status == "approved":
            send_mail(form.instance,"emails/approved_order.html","Pagamento Aprovado")
            redirect_url = "payments:success"
        elif status == "in_process":
            send_mail(form.instance,"emails/in_process_order.html","Pagamento Em analise")
            redirect_url = "payments:pending"

        elif status and status != "rejected":
            send_mail(form.instance,"emails/rejected_order.html","Pagamento Em Recusado")
            del self.request.session["order_id"]
        
        return redirect(redirect_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.order
        context["publishable_key"] = settings.MERCADO_PAGO_PUBLIC_KEY
        return context




class PaymentFailureView(TemplateView):
    template_name = "payments/failure.html"


class PaymentPendingView(TemplateView):
    template_name = "payments/pending.html"


class PaymentSuccessView(TemplateView):
    template_name = "payments/success.html"


@csrf_exempt
@require_POST
def payment_webhook(request):
    
    data = json.loads(request.body)
    form = UpdatePaymentForm(data)
    if form.is_valid():
        
        instance = form.save()
        status = instance.mercado_pago_status

        if status == "approved":
            send_mail(instance,"emails/email_confirmation.html","Pagamento Aprovado")
        
        elif status == "in_process":
            send_mail(instance,"emails/in_process_order.html","Pagamento Em analise")

        elif status and status != "rejected":
            send_mail(instance,"emails/rejected_order.html","Pagamento Recusado")

    return JsonResponse({})