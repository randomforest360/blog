# from django.views.generic import ListView, DetailView
# from .models import Term

# class TermListView(ListView):
#     model = Term
#     template_name = "glossary/term_list.html"
#     context_object_name = "terms"
#     paginate_by = 10  # show 10 terms per page

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         letter = self.request.GET.get('letter')
#         if letter:
#             queryset = queryset.filter(alphabet__iexact=letter)
#         else:
#             queryset = queryset.none()  # Show nothing if no letter selected
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Letters that have at least one term
#         context['letters'] = Term.objects.values_list('alphabet', flat=True).distinct().order_by('alphabet')
#         context['current_letter'] = self.request.GET.get('letter', '')
#         return context


# class TermDetailView(DetailView):
#     model = Term
#     template_name = "glossary/term_detail.html"
#     context_object_name = "term"
from django.views.generic import ListView, DetailView
from .models import Term

class TermListView(ListView):
    model = Term
    template_name = "glossary/term_list.html"
    context_object_name = "terms"
    paginate_by = 20  # show 10 terms per page

    def get_queryset(self):
        queryset = super().get_queryset().order_by('term')
        letter = self.request.GET.get('letter')

        if not letter:
            # Pick the first letter that has terms
            first_letter = Term.objects.values_list('alphabet', flat=True).distinct().order_by('alphabet').first()
            letter = first_letter or 'A'  # fallback to 'A' if glossary is empty

        self.current_letter = letter  # store for context
        queryset = queryset.filter(alphabet__iexact=letter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # All letters A-Z for navigation
        context['letters'] = [chr(i) for i in range(65, 91)]  # A-Z

        # Highlight only letters that actually have terms
        letters_with_terms = Term.objects.values_list('alphabet', flat=True).distinct()
        context['letters_with_terms'] = letters_with_terms

        # Current selected letter
        context['current_letter'] = getattr(self, 'current_letter', '')

        return context


class TermDetailView(DetailView):
    model = Term
    template_name = "glossary/term_detail.html"
    context_object_name = "term"

# from django.views.generic import ListView, DetailView
# from .models import Term

# class TermListView(ListView):
#     model = Term
#     template_name = "glossary/term_list.html"
#     context_object_name = "terms"
#     paginate_by = 50

# class TermDetailView(DetailView):
#     model = Term
#     template_name = "glossary/term_detail.html"
#     context_object_name = "term"
