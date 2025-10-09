# # lab/views.py
# from django.shortcuts import render, get_object_or_404
# from .models import LabItem

# def lab_list(request):
#     items = LabItem.objects.all().order_by('-created_at')
#     return render(request, "lab/lab_list.html", {"items": items})

# def lab_detail(request, pk):
#     item = get_object_or_404(LabItem, pk=pk)
#     return render(request, "lab/lab_detail.html", {"item": item})

from django.shortcuts import render

def lab_view(request):
    return render(request, 'lab/lab.html')
