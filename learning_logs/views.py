from django.shortcuts import render
from .models import Topic

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')
def topics(request): # topics() func takes request obj as param.
    """Show all topics."""
    topics = Topic.objects.order_by('date_added') # this is a db query. It's so clean!!
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context
