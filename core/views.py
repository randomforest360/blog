from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm
from content.models import Entry
from core.models import SocialLink
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.core import signing
from django.core.mail import send_mail
from django.conf import settings
from .forms import SubscribeForm
from .models import Subscriber

# class HomeView(TemplateView):
#     template_name = "core/home.html"

class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Latest 4 blog posts
        context["latest_posts"] = Entry.objects.filter(
            type="post", status="published"
        ).order_by("-created_at")[:6]

        # Only 1 latest featured project
        context["featured_project"] = Entry.objects.filter(
            type="project", status="published", is_featured=True
        ).order_by("-created_at").first()

        return context

class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        # Here you could send an email or save to DB
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        # Example: just show a success message
        messages.success(self.request, f"Thanks {name}, we received your message!")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add visible social links
        context["social_links"] = SocialLink.objects.filter(is_visible=True)
        return context
    

SIGNING_SALT = 'subscribe-salt'  # change to something unique in production

def send_verification_email(request, subscriber):
    token = signing.dumps({'email': subscriber.email}, salt=SIGNING_SALT)
    verify_url = request.build_absolute_uri(reverse('subscribe_verify', args=[token]))
    subject = "Confirm your subscription"
    message = (
        f"Hi — please confirm your subscription by clicking the link:\n\n{verify_url}\n\n"
        "If you didn't request this, ignore this email."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [subscriber.email])

def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            # honeypot check
            if form.cleaned_data.get('phone'):
                # likely spam — silently ignore or show generic message
                messages.success(request, "Thanks! Please check your email to confirm.")
                return redirect('subscribe')

            email = form.cleaned_data['email'].lower()
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            # if already active, notify; otherwise send verification
            if subscriber.is_active:
                messages.info(request, "You're already subscribed.")
                return redirect('subscribe')
            # send verification
            send_verification_email(request, subscriber)
            messages.success(request, "Check your email for a confirmation link.")
            return redirect('subscribe')
    else:
        form = SubscribeForm()
    return render(request, 'core/subscribe.html', {'form': form})

def subscribe_verify(request, token):
    try:
        data = signing.loads(token, salt=SIGNING_SALT, max_age=60*60*24*7)  # e.g. 7 days
        email = data.get('email')
    except signing.BadSignature:
        return HttpResponseBadRequest("Invalid or expired token.")
    subscriber = get_object_or_404(Subscriber, email=email)
    subscriber.is_active = True
    subscriber.save()
    messages.success(request, "Email verified — thank you! You're now subscribed.")
    return redirect('subscribe_thankyou')  # or render a thanks page


def thank_you_view(request):
    return render(request, 'core/subscribe_thankyou.html')



class PrivacyPolicyView(TemplateView):
    template_name = "core/privacy_policy.html"

class TermsOfServiceView(TemplateView):
    template_name = "core/terms_of_service.html"


class SupportView(TemplateView):
    template_name = "core/support.html"