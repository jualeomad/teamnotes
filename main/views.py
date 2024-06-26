from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from scripts.notes import Note
from scripts.services import create_note, get_notes_for_user_teams
from django.contrib.auth.decorators import login_required
from couchdb.client import Server
from teamnotes.settings import COUCHDB_DATABASE_NAME, COUCHDB_SERVER_URL

@login_required
def dashboard(request):
    user = request.user
    page = int(request.GET.get('page', 1))
    user_teams = request.user.teams
    query = request.GET.get('query', '')
    filter_by = request.GET.get('filter_by', 'title')
    
    daterange = request.GET.get('daterange')
    
    raw_query_params = request.GET.urlencode()

    all_notes, is_last_page = get_notes_for_user_teams(user_teams, page=page, query=query, filter_by=filter_by, daterange=daterange)
    is_first_page = page == 1
    
    return render(request, 'dashboard.html', {
        "all_notes": all_notes, 
        "is_first_page": is_first_page, 
        "is_last_page": is_last_page, 
        "current_page": page, 
        "user": user, 
        "query": query, 
        "filter_by": filter_by,
        "daterange": daterange,
        "raw_query_params": raw_query_params})


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


@login_required
def edit_note(request, note_id):
    raw_query_params = request.GET.urlencode()
    
    server = Server(COUCHDB_SERVER_URL)
    db = server[COUCHDB_DATABASE_NAME]
    note = db.get(note_id)

    if not note or note['team'] not in request.user.teams:
        return HttpResponseForbidden()

    if request.method == 'POST':
        note['title'] = request.POST.get('title', note['title'])
        note['content'] = request.POST.get('content', note['content'])
        note['team'] = request.POST.get('team', note['team'])
        db.save(note)
        return redirect(reverse('main:dashboard') + '?' + raw_query_params)

    return render(request, 'edit_note.html', {'note': note})

@login_required
def delete_note(request, note_id):
    raw_query_params = request.GET.urlencode()
    
    if request.method == 'POST':
        server = Server(COUCHDB_SERVER_URL)
        db = server[COUCHDB_DATABASE_NAME]
        note = db.get(note_id)

        if not note or note['team'] not in request.user.teams:
            return HttpResponseForbidden()

        if note:
            db.delete(note)

    return redirect(reverse('main:dashboard') + '?' + raw_query_params)
