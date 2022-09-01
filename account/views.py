from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, DeleteView, UpdateView, ListView, DetailView

from account.forms import RegisterForm, GroupForm, AddMemberToAdminForm, UserForm, UserProfileForm
from account.models import UserGroup, UserProfile, Admin


def index(request):
    return render(request, 'account/index.html')


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        if form.is_valid():
            messages.success(self.request, "Registration Successful...")
        return super(UserRegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('login')


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/password_change_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.request.session.flush()
        logout(self.request)
        return super(ChangePasswordView, self).form_valid(form)


class UpdateProfileView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user.userprofile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'account/updateprofile.html', context)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(self.request, f"{user.username} profile updated successfully...")
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'account/updateprofile.html')


class CreatGroupView(LoginRequiredMixin, FormView):
    form_class = GroupForm
    template_name = 'account/creategroup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if form.is_valid():
            group_form = form.save()
            group_form.user.add(self.request.user)
            group = UserGroup.objects.get(name=group_form.name)
            Admin.objects.create(user=self.request.user, group=group)
            messages.success(self.request, "Group created successfully..")
        return super(CreatGroupView, self).form_valid(form)


class AddAdminView(LoginRequiredMixin, FormView):
    form_class = AddMemberToAdminForm
    template_name = 'account/addtoadmin.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if form.is_valid():
            username = form.cleaned_data['username']
            group_name = form.cleaned_data['group_name']
            user = User.objects.get(username=username)
            group = UserGroup.objects.get(name=group_name)
            if group.user.all().filter(username=user.username).exists() and not Admin.objects.filter(user=user).filter(
                    group=group).exists():
                if Admin.objects.get(user=self.request.user, group=group) and Admin.objects.filter(
                        user__admin__group=group).count() < 3:
                    Admin.objects.create(user=user, group=group)
                    messages.success(self.request, f'{username} has been added as an admin')
                else:
                    messages.error(self.request, 'You are not an admin or Group admin is upto 3')
                    return HttpResponseRedirect(reverse('addtoadmin'))
            else:
                messages.error(self.request,
                               f'{username} is not member of the group or is an admin of the group before')
                return HttpResponseRedirect(reverse('addtoadmin'))
        return super(AddAdminView, self).form_valid(form)


class RemoveMemberOfTheGroup(LoginRequiredMixin, FormView):
    form_class = AddMemberToAdminForm
    template_name = 'account/remove-member.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        if form.is_valid():
            username = form.cleaned_data['username']
            group_name = form.cleaned_data['group_name']
            user = User.objects.get(username=username)
            group = UserGroup.objects.get(name=group_name)
            if group.user.all().filter(username=user.username).exists():
                if Admin.objects.filter(user=self.request.user, group=group).exists():
                    group.user.remove(user)
                    group.save()
                    messages.success(self.request, f"{username} removed successfully..")
                    return HttpResponseRedirect(reverse('index'))
                else:
                    messages.error(self.request, "You're not the admin of the group..")
                    return HttpResponseRedirect(reverse('remove-member'))
            else:
                messages.error(self.request, f'{username} is not member of the group..')
                return HttpResponseRedirect(reverse('remove-member'))
        return super(RemoveMemberOfTheGroup, self).form_valid(form)


class GroupListView(LoginRequiredMixin, ListView):
    model = UserGroup
    template_name = 'account/grouplist.html'
    context_object_name = 'grouplist'

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search is not None:
            queryset = UserGroup.objects.filter(name__iexact=search)
        else:
            queryset = UserGroup.objects.all()
        return queryset


class MemberJoinGroupView(View):
    def post(self, request, pk, grouppk):
        group = UserGroup.objects.get(pk=grouppk)
        user = User.objects.get(pk=pk)
        if not group.user.filter(username=user.username).exists():
            group.user.add(user)
            messages.success(self.request, f'{user.username} joined {group.name} group successfully.')
            return HttpResponseRedirect(reverse('group-list'))
        else:
            group.user.remove(user)
            messages.success(self.request, "You're successfully exit the group.")
            return HttpResponseRedirect(reverse('group-list'))


class MemberListView(LoginRequiredMixin, DetailView):
    model = UserGroup
    template_name = 'account/memberlist.html'
    context_object_name = 'group_detail'
