from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ContactForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse




@login_required # decorator to ensure user is logged in


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Perform actions (e.g., send email)
            return redirect('polls:thanks')
    else:
        form = ContactForm()
    return render(request, 'polls/contact.html', {'form': form})


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    paginator = Paginator(latest_question_list, 5) # Show 5 questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'polls/index.html', {'page_obj': page_obj})

# class Base approch 
# from django.views import View
# from django.http import HttpResponse

# class IndexView(View):
#     def get(self, request):
#         return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, question_id):
    # View to display a specific question
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    # View to display the results of a specific question
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Increment the vote count and save
        selected_choice.votes += 1
        selected_choice.save()
        # Redirect to the results page after successful vote
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    

def json_example(request):
    data = {
        'message': 'Hello, World!',
        'items': [1, 2, 3, 4, 5],
    }
    return JsonResponse(data)

def trigger_error(request):
    # Simulate an error by dividing by zero
    result = 1 / 0
    raise Exception("This is a simulated server error!")
    return HttpResponse("This will never be reached.")