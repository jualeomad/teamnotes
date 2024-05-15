from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from scripts.services import create_note, get_all_notes

def dashboard(request):
    all_notes = get_all_notes()
    return render(request, 'dashboard.html', {"all_notes": all_notes})

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
