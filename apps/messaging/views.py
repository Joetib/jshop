from django.contrib import staticfiles
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.http.request import HttpRequest
from apps.store.models import Product
from django.http.response import HttpResponse
from django.contrib import messages
from apps.messaging.models import Sms
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .forms import SmsForm
from bs4 import BeautifulSoup
from django.contrib.staticfiles import finders
from django.contrib.sites.models import Site
from django.utils import timezone

# Create your views here.


class HomePage(TemplateView):
    template_name = "messaging/homepage.html"


class SmsListView(ListView):
    model = Sms
    paginate_by = 24
    context_object_name = "sms_messages"
    template_name = "messaging/sms_list.html"


class SmsDetailView(DetailView):
    model = Sms
    context_object_name = "sms_message"
    template_name = "messaging/sms_detail.html"


def create_sms(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        sms_form = SmsForm(request.POST)
        if sms_form.is_valid():
            sms: Sms = sms_form.save()
            if not sms.is_draft:
                sent = sms.send_sms()
                if sent:
                    messages.success(request, "Sms sent successfully")
                else:
                    messages.error(request, "Sorry, could not send sms")
            else:
                messages.success(request, "Sms has been saved as draft.")
    else:
        sms_form = SmsForm()
    return render(request, "messaging/create_sms.html", {"sms_form": sms_form})


def send_email(request: HttpRequest):
    title = request.GET.get("title", "Hello welcome to " + str(timezone.now()))
    site= Site.objects.first()
    
    email = render_to_string(
        "emails/test.html",
        context={
            "products": Product.objects.all(),
            "sms_messages": Sms.objects.all(),
            "host_name": site.domain.strip('/'),
        },
    )
    soup = BeautifulSoup(email)
    
    send_mail(
        subject=title,
        message=soup.get_text(),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["otiboatengjoe@gmail.com"],
        html_message=email,
    )
    files = finders.find("css/base.css")
    return redirect("messaging:sms-list")