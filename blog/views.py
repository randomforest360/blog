from django.shortcuts import render
from django.views.generic import ListView, DetailView
from content.models import Entry, EntryCategory, EntryTag, EntryLike
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse





class PostListView(ListView):
    model = Entry
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.filter(type='post', status='published').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Featured posts
        context["featured_posts"] = Entry.objects.filter(
            type="post",
            status="published",
            is_featured=True
        ).order_by("-created_at")[:3]

        # Only categories and tags used by published posts
        post_qs = Entry.objects.filter(type='post', status='published')

        # Categories used by posts
        context["all_categories"] = EntryCategory.objects.filter(
            entry_categories__in=post_qs
        ).distinct().order_by('name')

        # Tags used by posts
        context["all_tags"] = EntryTag.objects.filter(
            entry_tags__in=post_qs
        ).distinct().order_by('name')

        return context


class PostDetailView(DetailView):
    model = Entry
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Entry.objects.filter(type='post', status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["post"]

        # --- TOC generation ---
        soup = BeautifulSoup(post.body, "lxml")
        toc_headings = []
        for index, tag in enumerate(soup.find_all(["h2", "h3"])):
            tag_id = tag.get("id") or f"section-{index}"
            tag["id"] = tag_id
            toc_headings.append({
                "text": tag.get_text(),
                "id": tag_id,
                "level": tag.name
            })
        post.body = mark_safe(str(soup))
        context["toc_headings"] = toc_headings

        # --- Anonymous like detection ---
        request = self.request
        ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0] or request.META.get("REMOTE_ADDR")
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        liked_by_user = EntryLike.objects.filter(
            entry=post,
            ip_address=ip,
            session_key=session_key
        ).exists()
        context["liked_by_user"] = liked_by_user

        # --- Featured posts ---
        context["featured_posts"] = Entry.objects.filter(
            type="post",
            status="published",
            is_featured=True
        ).order_by("-created_at")[:3]

        # --- Categories and tags ---
        post_qs = Entry.objects.filter(type='post', status='published')
        all_categories = EntryCategory.objects.filter(entry_categories__in=post_qs).distinct().order_by('name')
        all_tags = EntryTag.objects.filter(entry_tags__in=post_qs).distinct().order_by('name')
        category_tags_map = {
            category.slug: EntryTag.objects.filter(categories=category, entry_tags__in=post_qs).distinct()
            for category in all_categories
        }

        context["all_categories"] = all_categories
        context["all_tags"] = all_tags
        context["category_tags_map"] = category_tags_map

        return context





POSTS_PER_PAGE = 10  # adjust if needed
def post_search(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    # Base queryset
    post_list = Entry.objects.filter(
        type='post',
        status__in=['in_progress', 'published']
    ).select_related('author').prefetch_related('categories', 'tags', 'links')

    # Filter by query
    if query:
        post_list = post_list.filter(title__icontains=query)

    # Filter by category
    selected_category = None
    if category_slug:
        post_list = post_list.filter(categories__slug=category_slug)
        selected_category = get_object_or_404(EntryCategory, slug=category_slug)

    # selected_category = None
    # if category_slug:
    #     selected_category = get_object_or_404(EntryCategory, slug=category_slug)
    #     post_list = post_list.filter(categories=selected_category)

    # Final ordering
    post_list = post_list.order_by('-created_at')

    # Pagination
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Sidebar filters based on filtered results
    all_categories = EntryCategory.objects.filter(entry_categories__in=post_list).distinct().order_by('name')
    filtered_tags = EntryTag.objects.filter(entry_tags__in=post_list).distinct().order_by('name')

    context = {
        'query': query,
        'page_obj': page_obj,
        'all_categories': all_categories,
        'filtered_tags': filtered_tags,
        'selected_category': selected_category,
        
    }
    return render(request, 'blog/search_results.html', context)




def post_category(request, slug):
    current_category = get_object_or_404(EntryCategory, slug=slug)

    post_list = Entry.objects.filter(
        type='post',
        status__in=['in_progress', 'published'],
        categories=current_category,
    ).select_related('author').prefetch_related('categories', 'tags', 'links').order_by('-created_at')

    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # All categories used by posts
    posts_qs = Entry.objects.filter(type='post', status__in=['in_progress', 'published'])
    all_categories = EntryCategory.objects.filter(entry_categories__in=posts_qs).distinct().order_by('name')

    # Tags linked to current category
    category_tags = EntryTag.objects.filter(categories=current_category, entry_tags__in=posts_qs).distinct().order_by('name')

    return render(
        request,
        'blog/category.html',
        {
            'page_obj': page_obj,
            'current_category': current_category,
            'all_categories': all_categories,
            'category_tags': category_tags,
            
        },
    )


def post_tag(request, slug):
    current_tag = get_object_or_404(EntryTag, slug=slug)

    # Filter posts by the tag using the field name
    post_list = (
        Entry.objects.filter(
            type='post',
            status__in=['in_progress', 'published'],
            tags=current_tag,  # use the field name on Entry, NOT related_name
        )
        .select_related('author')
        .prefetch_related('categories', 'tags', 'links')
        .order_by('-created_at')
    )

    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Restrict categories/tags to posts only
    posts_qs = Entry.objects.filter(
        type='post',
        status__in=['in_progress', 'published'],
    )

    all_categories = (
        EntryCategory.objects.filter(entry_categories__in=posts_qs)
        .distinct()
        .order_by('name')
    )
    all_tags = (
        EntryTag.objects.filter(entry_tags__in=posts_qs)
        .distinct()
        .order_by('name')
    )

    return render(
        request,
        'blog/tag.html',
        {
            'page_obj': page_obj,
            'current_tag': current_tag,  # pass this for template highlighting
            'all_categories': all_categories,
            'all_tags': all_tags,
        },
    )



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

def like_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    ip = get_client_ip(request)
    session_key = request.session.session_key or request.session.save() or request.session.session_key

    like, created = EntryLike.objects.get_or_create(
        entry=entry,
        ip_address=ip,
        session_key=session_key
    )

    if created:
        entry.likes_count += 1
        entry.save()

    return JsonResponse({'likes': entry.likes_count})



def post_category_tag(request, category_slug, tag_slug):
    category = get_object_or_404(EntryCategory, slug=category_slug)
    tag = get_object_or_404(EntryTag, slug=tag_slug)

    # Filter posts by category and tag
    posts = Entry.objects.filter(
        type="post",
        status="published",
        categories=category,
        tags=tag
    ).order_by("-created_at")

    # Paginate results
    paginator = Paginator(posts, 9)  # Show 9 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get tags used in posts within this category
    category_tags = EntryTag.objects.filter(
        entry_tags__type="post",
        entry_tags__status="published",
        entry_tags__categories=category
    ).distinct()

    all_categories = EntryCategory.objects.all()

    return render(request, "blog/post_list.html", {
        "page_obj": page_obj,
        "current_category": category,
        "current_tag": tag,
        "category_tags": category_tags,
        "all_categories": all_categories,
    })


