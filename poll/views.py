import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

# Create your views here.
from django.urls import reverse

from groups.models import Member, Group
from poll.forms import PollForm, ChoiceForm, PollInlineFormSet
from poll.models import Poll, Choice, Voter


def create_poll(request, pk):
    group = Group.objects.get(pk=pk)
    PollFormSet = inlineformset_factory(
        Poll, Choice, form=ChoiceForm, extra=4, can_delete=False)

    if group.group_member.filter(member=request.user).exists():
        if group.group_member.get(member=request.user).is_admin:

            if request.method == 'POST':
                form = PollForm(request.POST)
                choice_form = PollFormSet(request.POST, instance=form.instance)

                if choice_form.is_valid() and form.is_valid():
                    form = form.save(commit=False)
                    member = group.group_member.get(member=request.user)
                    form.creator = member
                    form.group = group
                    form.save()
                    choice_form.save()
                    messages.success(request, 'Poll saved..')
                    return redirect('group-detail', group.id)
                messages.error(request, 'Invalid form')
                return redirect('poll:create-poll', group.id)
            form = PollForm()
            choice_form = PollFormSet()
            return render(request, 'poll/create-poll.html', {'form': form, 'choice_form': choice_form, 'group': group})

        else:
            messages.error(request, 'You are not an admin of the group')
            return render(request, 'groups/group_detail.html')
    else:
        messages.error(request, "You're not member of the group")
        return redirect('group-detail', group.id)


def poll_detail(request, pk, poll_pk):
    group = Group.objects.get(pk=pk)
    poll = group.poll_set.get(pk=poll_pk)
    return render(request, 'poll/poll-detail.html', {'poll': poll, 'group': group})


def edit_poll(request, group_pk, poll_pk):
    group = Group.objects.get(pk=group_pk)
    poll = group.poll_set.get(pk=poll_pk)
    choice = Choice.objects.filter(poll=poll)
    choice_objects = list()
    for c in choice:
        choice_objects.append(c)

    pollform = PollInlineFormSet(instance=poll)
    pol_form = PollForm(instance=poll)

    if group.group_member.get(member=request.user).is_admin:
        if poll.start_date > datetime.date.today():
            if request.method == 'POST':
                poll_form = PollForm(request.POST, instance=poll)
                choice_form = PollInlineFormSet(request.POST, instance=poll)


                if poll_form.is_valid() and choice_form.is_valid():
                    poll_form.save()
                    choice_form.save()
                    messages.success(request, "Update Successful...")
                    return redirect('group-detail', group.id)
            context = {
                'group': group,
                'pol': poll,
                'choices': choice_objects,
                'choice2': choice_objects[1],
                # 'choice3': choice_objects[2],
                'pollform': pollform,
                'pol_form': pol_form,
            }
            return render(request, 'poll/edit-poll.html', context)

        else:
            messages.error(request, 'You can only edit before the start date.')
            return redirect('group-detail', group.id)
    else:
        messages.error(request, "Only admin can edit the poll..")
        return redirect('group-detail', group.id)


def vote(request, pk):
    poll = Poll.objects.get(pk=pk)
    group = Group.objects.get(poll=poll)
    if group.group_member.filter(member=request.user).exists():
        member = group.group_member.get(member=request.user)
        # print(member)
        # member = Member.objects.get(pk=request.user.id)
        voter = member.voter_set.filter(poll=poll)

        if not member.is_suspended:
            if not voter.exists():
                try:
                    selected_choice = poll.choice_set.get(
                        pk=request.POST['poll.choice_set'])
                except (KeyError, poll.DoesNotExist):
                    return render(request, 'poll/poll-detail.html', {
                        "poll": poll,
                        "error_message": "You didn't select a choice."
                    })
                else:
                    selected_choice.vote += 1
                    selected_choice.save()
                    save_voter = Voter.objects.create(member=member)
                    save_voter.poll.add(poll)
                    messages.success(request, 'Successful...')
                    return HttpResponseRedirect(reverse('group-detail', args=[group.id]))
            else:
                messages.error(request, 'You have voted')
                return redirect('poll:poll-detail', group.id, poll.id)
        else:
            messages.error(request, 'You have suspended.')
            return redirect('poll:poll-detail', group.id, poll.id)
    else:
        messages.error(request, "You are not the member of the group.")
        return redirect('poll:poll-detail', group.id, poll.id)


def poll_summary(request, group_pk, poll_pk):
    group = Group.objects.get(pk=group_pk)
    poll = group.poll_set.get(pk=poll_pk)
    today = datetime.date.today()
    member = group.group_member.get(member=request.user)
    end_date = poll.end_date

    return render(request, 'poll/poll-summary.html',
                  {'poll': poll, 'group': group, 'today': today, 'member': member, 'end_date': end_date})
