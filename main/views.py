from django.shortcuts import render

from scripts.services import get_all_notes

# Create your views here.
def example(request):
    
    all_notes = get_all_notes()
    
    print(all_notes)
    
    
    return render(request, 'example.html', {"all_notes": all_notes})