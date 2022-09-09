from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone

from groups.models import Member, Group
from poll.forms import PollForm
from poll.models import Poll


def create_poll(request, pk):
    group = Group.objects.get(pk)
    member = group.group_member.get(request.user.id)
    if member.is_admin:
        if request.method == 'POST':
            form = PollForm(request.POST)

            if form.is_valid():
                poll_form = form.save(commit=False)
                poll_form.creator = request.user
                poll_form.group = group
                poll_form.save()
                return redirect('poll-list')
            messages.error(request, 'Invalid form')
        form = PollForm()
        return render(request, 'poll/create-poll.html', {'form': form})
    else:
        messages.error(request, 'You are not an admin of the group')


def edit_poll(request, group_pk, poll_pk):
    group = Group.objects.get(pk=group_pk)
    poll = group.poll_set.get(poll_pk)
    pol_form = PollForm(instance=poll)

    if poll.start_date > timezone.now():
        if request.method == 'POST':
            poll_form = PollForm(request.POST, instance=poll)

            if poll_form.is_valid():
                poll_form.save()
                return redirect('poll-list')
        context = {
            'group': group,
            'poll': poll,
            'pol_form': pol_form,
        }
        return render(request, 'poll/poll-detail.html', context)
    else:
        messages.error(request, 'You can only edit before the start date.')


def vote(request, pk):
    poll = Poll.objects.get(pk=pk)
    member = Member.objects.get(pk=request.user.id)

    if not member.is_suspended:
        try:
            selected_choice = poll.choice_set.get(pk=request.POST)
        except (KeyError, poll.DoesNotExist):
            return render(request, 'poll/poll-detail.html', {
                "poll": poll,
                "error_message": "You didn't select a choice."
            })
        else:
            selected_choice.vote += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('detail', args=[pk]))
