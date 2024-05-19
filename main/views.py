from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from scripts.services import create_note, get_all_notes
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    
    page = int(request.GET.get('page', 1))
    
    all_notes, is_last_page = get_all_notes(page=page)
    
    is_first_page = page == 1
    
    return render(request, 'dashboard.html', {"all_notes": all_notes, "is_first_page": is_first_page, "is_last_page": is_last_page, "current_page": page})

@login_required
def create_note_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user.username
        
        if not title.strip():
            return render(request, 'create_note.html', {'error_message': "Title cannot be empty"})
        
        create_note(title, content, author)
        return redirect('main:dashboard')
    
    return render(request, 'create_note.html')
