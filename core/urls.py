from django.urls import path
from .views import HomeView, AboutView, ContactView, PrivacyPolicyView, TermsOfServiceView, SupportView
from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('subscribe/verify/<str:token>/', views.subscribe_verify, name='subscribe_verify'),
    path('subscribe/thanks/', views.thank_you_view, name='subscribe_thankyou'),  # optional
    path("privacy/", PrivacyPolicyView.as_view(), name="privacy_policy"),
    path("terms/", TermsOfServiceView.as_view(), name="terms_of_service"),
    path("terms/", TermsOfServiceView.as_view(), name="terms_of_service"),
    path('support/', SupportView.as_view(), name='support'),
]
