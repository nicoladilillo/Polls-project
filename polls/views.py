from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from registration.signals import user_registered
from django.utils import timezone

from .models import Choice, Question, Voter


def index(request):
    question = Question.objects.order_by('-pub_date')
    return render(request, 'polls/index.html', {'question': question, 'timezone': timezone.now })


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user.is_authenticated() and question.end_date > timezone.now():
        return render(request, 'polls/detail.html', {'question': question})
    else:
        return render(request, 'polls/results.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Vote only once
    if Voter.objects.filter(poll_id=question_id, user_id=request.user.id).exists():
        return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "Sorry, but you have already voted."
        })
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        v = Voter(user=request.user, poll=question)
        v.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
