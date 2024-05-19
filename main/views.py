from django.shortcuts import render, redirect
from scripts.services import create_note, get_notes_for_user_teams
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    page = int(request.GET.get('page', 1))
    user_teams = request.user.teams
    all_notes, is_last_page = get_notes_for_user_teams(user_teams, page=page)
    is_first_page = page == 1
    return render(request, 'dashboard.html', {"all_notes": all_notes, "is_first_page": is_first_page, "is_last_page": is_last_page, "current_page": page})

@login_required
def create_note_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        team = request.POST.get('team')
        author = request.user.username
        
        if not title.strip():
            return render(request, 'create_note.html', {'error_message': "Title cannot be empty"})
        
        if not team.strip():
            return render(request, 'create_note.html', {'error_message': "Team cannot be empty"})
        
        create_note(title, content, author, team)
        return redirect('main:dashboard')
    
    return render(request, 'create_note.html')
