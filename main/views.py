from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from scripts.services import create_note, get_all_notes


from scripts.services import get_all_notes

# Create your views here.

def dashboard(request):
    
    page = int(request.GET.get('page', 1))
    
    all_notes, is_last_page = get_all_notes(page=page)
    
    is_first_page = page == 1
    
    return render(request, 'dashboard.html', {"all_notes": all_notes, "is_first_page": is_first_page, "is_last_page": is_last_page, "current_page": page})

def create_note_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        
        if title and content and author:
            create_note(title, content, author)
            return redirect('main:dashboard')
        else:
            return HttpResponseBadRequest("Invalid form data")
    
    return render(request, 'create_note.html')
