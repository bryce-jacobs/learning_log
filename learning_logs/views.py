from django.shortcuts import render, redirect
# import classes from the .py files that I wrote in the learning_logs dir.
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# func for check if user has perms
def check_topic_owner(request, topic):
    if request.user != topic.owner:
        raise Http404

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request): # topics() func takes request obj as param.
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added') # this is a db query. It's so clean!!
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # stop other users from accessing user specific content.
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add new topic"""
    if request.method != 'POST':
        # if request is not POST, it is probably GET, so return a blank copy of the form.
        form = TopicForm()
    else:
        # process the submitted data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # i feel like this is a cheeky hack to edit fields on a form.
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            # create entry in db with data in form.
            new_topic.save()
            # upon saveing their entry, redirect user to topics page.
            return redirect('learning_logs:topics')
    # if the request was not to post or the form was invalid, display blank or invalid form
    context = {'form': form}
    # pass the request obj into the right func in views.py and also feed in either
    # a blank form, or the invalid form that the user submitted
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # There is no option for the user to specify the topic (on the form),
            # and it would be bad practice to make the user do that. So we 
            # save the info they put into the form in an obj of the type of a db
            # entry. Then we modify the topic automatically. Now we can insert to
            # db.
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
