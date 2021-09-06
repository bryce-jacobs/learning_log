from django.shortcuts import render, redirect
# import classes from the .py files that I wrote in the learning_logs dir.
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')
def topics(request): # topics() func takes request obj as param.
    """Show all topics."""
    topics = Topic.objects.order_by('date_added') # this is a db query. It's so clean!!
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
def new_topic(request):
    """Add new topic"""
    if request.method != 'POST':
        # if request is not POST, it is probably GET, so return a blank copy of the form.
        form = TopicForm()
    else:
        # process the submitted data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # create entry in db with data in form.
            form.save()
            # upon saveing their entry, redirect user to topics page.
            return redirect('learning_logs:topics')

    # if the request was not to post or the form was invalid, display blank or invalid form
    context = {'form': form}
    # pass the request obj into the right func in views.py and also feed in either
    # a blank form, or the invalid form that the user submitted
    return render(request, 'learning_logs/new_topic.html', context)
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
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
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
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
