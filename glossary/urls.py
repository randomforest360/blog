from django.urls import path
from . import views

app_name = "glossary"

urlpatterns = [
    # List all terms or filtered by letter via GET parameter ?letter=A
    path("", views.TermListView.as_view(), name="term_list"),

    # Detail page for a term
    path("term/<slug:slug>/", views.TermDetailView.as_view(), name="term_detail"),
]
