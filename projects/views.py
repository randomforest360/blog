from django.shortcuts import render
from django.views.generic import ListView, DetailView
from content.models import Entry, EntryTag
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

PROJECTS_PER_PAGE = 10
FEATURED_PROJECTS = 3

class ProjectListView(ListView):
    model = Entry
    template_name = "projects/index.html"
    context_object_name = "projects"
    paginate_by = PROJECTS_PER_PAGE

    def get_queryset(self):
        return Entry.objects.filter(type='project', status='published').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # --- Featured projects ---
        context["featured_projects"] = Entry.objects.filter(type="project", status="published", is_featured=True).order_by("-created_at")[:FEATURED_PROJECTS]

        # --- Tags used by published projects ---
        project_qs = Entry.objects.filter(type='project', status='published')
        context["all_tags"] = EntryTag.objects.filter(entry_tags__in=project_qs).distinct().order_by('name')

        return context


class ProjectDetailView(DetailView):
    model = Entry
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Entry.objects.filter(type='project', status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = context["project"]

        # --- TOC generation ---
        soup = BeautifulSoup(project.body, "lxml")
        toc_headings = []
        for index, tag in enumerate(soup.find_all(["h2", "h3"])):
            tag_id = tag.get("id") or f"section-{index}"
            tag["id"] = tag_id
            toc_headings.append({
                "text": tag.get_text(),
                "id": tag_id,
                "level": tag.name
            })
        project.body = mark_safe(str(soup))
        context["toc_headings"] = toc_headings

        # --- Featured projects ---
        context["featured_projects"] = Entry.objects.filter(type="project", status="published", is_featured=True).order_by("-created_at")[:FEATURED_PROJECTS]

        # --- Tags used by published projects ---
        project_qs = Entry.objects.filter(type='project', status='published')
        context["all_tags"] = EntryTag.objects.filter(entry_tags__in=project_qs).distinct().order_by('name')

        return context


# -----------------------------
# Search projects by title only
# -----------------------------
def project_search(request):
    query = request.GET.get('q', '').strip()

    # Base queryset
    project_list = Entry.objects.filter(
        type='project',
        status__in=['published']
    ).select_related('author').prefetch_related('tags', 'links')

    # Filter by title query
    if query:
        project_list = project_list.filter(title__icontains=query)

    # Final ordering
    project_list = project_list.order_by('-created_at')

    # Pagination
    paginator = Paginator(project_list, PROJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all tags for sidebar
    all_tags = EntryTag.objects.filter(entry_tags__in=project_list).distinct().order_by('name')

    context = {
        'query': query,
        'page_obj': page_obj,
        'all_tags': all_tags,
    }
    return render(request, 'projects/search_results.html', context)


# -----------------------------
# Filter projects by tag
# -----------------------------
def project_tag(request, slug):
    current_tag = get_object_or_404(EntryTag, slug=slug)

    project_list = (
        Entry.objects.filter(
            type='project',
            status='published',
            tags=current_tag,
        )
        .select_related('author')
        .prefetch_related('tags', 'links')
        .order_by('-created_at')
    )

    # Pagination
    paginator = Paginator(project_list, PROJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # All tags for sidebar
    all_tags = EntryTag.objects.filter(entry_tags__in=Entry.objects.filter(type='project', status='published')).distinct().order_by('name')

    context = {
        'page_obj': page_obj,
        'current_tag': current_tag,
        'all_tags': all_tags,
    }
    return render(request, 'projects/tag.html', context)




