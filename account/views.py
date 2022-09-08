from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, FormView, DeleteView, UpdateView, ListView, DetailView

from account.forms import RegisterForm, UserProfileForm
from account.models import User, UserProfile
from account.utils import send_email_verification


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            send_email_verification(self.request, user)
            messages.success(
                self.request, "Registration Successful... Check your mail to activate the account. ")
            return redirect('login')


def activate(request, uidb64, token):
    try:
        user_pk = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=user_pk)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request, "Congratulations! Your account is activated.")
        return redirect('index')

    else:
        messages.error(request, "Invalid Activation Link!")
        return redirect('login')


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/password_change_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.request.session.flush()
        logout(self.request)
        return super(ChangePasswordView, self).form_valid(form)


class UpdateProfileView(UpdateView):
    model = User
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse('update-profile', kwargs={'pk': self.kwargs.get('pk')})


# @login_required(login_url='login')
def edit_profile(request, profile_pk):
    # user_profile = UserProfile.objects.get(pk=profile_pk)
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        profile_form = UserProfileForm(
            request.POST, request.FILES)
        print(user_form.errors)
        print(profile_form.errors)
        if user_form.is_valid() and profile_form.is_valid():
            print("Did it")
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Update was saved successfully")
            print("Here")
            return redirect(reverse('update-profile', args=[profile_pk]))

    else:
        user_form = RegisterForm(instance=request.user)
        profile_form = UserProfileForm()
    context = {
        "user_form": user_form,
        "profile_form": profile_form
    }

    return render(request, 'account/user_form.html', context)
# class CreatGroupView(LoginRequiredMixin, FormView):
#     form_class = GroupForm
#     template_name = 'account/creategroup.html'
#     success_url = reverse_lazy('index')

#     def form_valid(self, form):
#         if form.is_valid():
#             group_form = form.save()
#             group_form.user.add(self.request.user)
#             group = Group.objects.get(name=group_form.name)
#             Admin.objects.create(user=self.request.user, group=group)
#             messages.success(self.request, "Group created successfully..")
#         return super(CreatGroupView, self).form_valid(form)


# class AddAdminView(LoginRequiredMixin, FormView):
#     form_class = AddMemberToAdminForm
#     template_name = 'account/addtoadmin.html'
#     success_url = reverse_lazy('index')

#     def form_valid(self, form):
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             group_name = form.cleaned_data['group_name']
#             user = User.objects.get(username=username)
#             group = Group.objects.get(name=group_name)
#             if group.user.all().filter(username=user.username).exists() and not Admin.objects.filter(user=user).filter(
#                     group=group).exists():
#                 if Admin.objects.get(user=self.request.user, group=group) and Admin.objects.filter(
#                         user__admin__group=group).count() < 3:
#                     Admin.objects.create(user=user, group=group)
#                     messages.success(
#                         self.request, f'{username} has been added as an admin')
#                 else:
#                     messages.error(
#                         self.request, 'You are not an admin or Group admin is upto 3')
#                     return HttpResponseRedirect(reverse('addtoadmin'))
#             else:
#                 messages.error(self.request,
#                                f'{username} is not member of the group or is an admin of the group before')
#                 return HttpResponseRedirect(reverse('addtoadmin'))
#         return super(AddAdminView, self).form_valid(form)


# class RemoveMemberOfTheGroup(LoginRequiredMixin, FormView):
#     form_class = AddMemberToAdminForm
#     template_name = 'account/remove-member.html'
#     success_url = reverse_lazy('index')

#     # def form_valid(self, form):
#     #     if form.is_valid():
#     #         username = form.cleaned_data['username']
#     #         group_name = form.cleaned_data['group_name']
#     #         user = User.objects.get(username=username)
#     #         group = UserGroup.objects.get(name=group_name)
#     #         if group.user.all().filter(username=user.username).exists():
#     #             if Admin.objects.filter(user=self.request.user, group=group).exists():
#     #                 group.user.remove(user)
#     #                 group.save()
#     #                 messages.success(
#     #                     self.request, f"{username} removed successfully..")
#     #                 return HttpResponseRedirect(reverse('index'))
#     #             else:
#     #                 messages.error(
#     #                     self.request, "You're not the admin of the group..")
#     #                 return HttpResponseRedirect(reverse('remove-member'))
#     #         else:
#     #             messages.error(
#     #                 self.request, f'{username} is not member of the group..')
#     #             return HttpResponseRedirect(reverse('remove-member'))
#     #     return super(RemoveMemberOfTheGroup, self).form_valid(form)


# class GroupListView(LoginRequiredMixin, ListView):
#     pass
#     # model = UserGroup
#     # template_name = 'account/grouplist.html'
#     # context_object_name = 'grouplist'

#     # def get_queryset(self):
#     #     # search = self.request.GET.get('search')
#     #     # if search is not None:
#     #     #     queryset = UserGroup.objects.filter(name__iexact=search)
#     #     # else:
#     #     #     queryset = UserGroup.objects.all()
#     #     return queryset


# class MemberJoinGroupView(View):
#     def post(self, request, pk, grouppk):
#         pass
#         # group = UserGroup.objects.get(pk=grouppk)
#         # user = User.objects.get(pk=pk)
#         # if not group.user.filter(username=user.username).exists():
#         #     group.user.add(user)
#         #     messages.success(
#         #         self.request, f'{user.username} joined {group.name} group successfully.')
#         #     return HttpResponseRedirect(reverse('group-list'))
#         # else:
#         #     group.user.remove(user)
#         #     messages.success(
#         #         self.request, "You're successfully exit the group.")
#         #     return HttpResponseRedirect(reverse('group-list'))


# class MemberListView(LoginRequiredMixin, DetailView):
#     pass
#     #     pass
#     # model = UserGroup
#     # template_name = 'account/memberlist.html'
#     # context_object_name = 'group_detail'
