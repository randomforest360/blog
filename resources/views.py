from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Resource, ResourceCategory

# -----------------------------
# Resource List / Homepage
# -----------------------------
class ResourceListView(ListView):
    model = Resource
    template_name = "resources/resource_list.html"
    context_object_name = "resources"
    ordering = ["-is_featured", "title"]
    paginate_by = 24  # optional, nice for big lists


# -----------------------------
# Resource Detail
# -----------------------------
class ResourceDetailView(DetailView):
    model = Resource
    template_name = "resources/resource_detail.html"
    context_object_name = "resource"


# -----------------------------
# Category View
# -----------------------------
def category_detail(request, slug):
    category = get_object_or_404(ResourceCategory, slug=slug)
    resources = category.resources.order_by("-is_featured", "title")
    return render(
        request,
        "resources/category_detail.html",
        {"category": category, "resources": resources},
    )
