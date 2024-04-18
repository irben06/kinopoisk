from django.shortcuts import render
from .forms import ContactForm
from django.views.generic import CreateView
# Create your views here.

class ContactView(CreateView):
    model = ContactForm
    form_class = ContactForm
    success_url = "/"