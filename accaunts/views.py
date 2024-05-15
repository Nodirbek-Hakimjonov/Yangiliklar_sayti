from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .models import Profile
from .forms import LoginForm, UserEditForm, ProfileEditForm, UserRegistrationForm


def user_login(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request,
                              username=data['username'],
                              password=data['password'],)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Muvaffaqiyatli login amalga oshirildi!')
                else:
                    return HttpResponse('Sizning profilingiz faol holatda emas!')
            else:
                return HttpResponse('Login va parolda xatolik bor')
    else:
        form=LoginForm()
        context={
            'form':form
        }
    return render(request,'registration/login.html',context=context)

from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return render(request,template_name='registration/logged_out.html')
    # Redirect to a success page.

@login_required
def dashboard_view(request):
    user=request.user
    # profile_info=Profile.objects.get(user=user)
    profile_info=get_object_or_404(Profile,user=user)
    context={
        'user':user,
        'profile':profile_info,
    }
    return render(request,template_name='pages/dashboard.html',context=context)
from .tasks import send_email
# def user_register(request):
#     if request.method == 'POST':
#         user_form=UserregistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user=user_form.save(commit=False)
#             new_user.set_password(
#                 user_form.cleaned_data['password']
#             )
#             new_user.save()
#             Profile.objects.create(user=new_user)
#             context={
#                 'new_user':new_user,
#             }
#             return render(request,'accaunt/register_done.html',context=context)
#     else:
#         user_form=UserregistrationForm()
#         print(user_form)
#         context={
#             'user_form':user_form
#         }
#         return render(request,'accaunt/register.html',context=context)
# def user_register(request):
#     if request.method=='POST':
#         user_form=UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user=user_form.save(commit=False)
#             new_user.set_password(
#                 user_form.cleaned_data['password']
#             )
#             new_user.save()
#             Profile.objects.create(user=new_user)
#             context={
#                 'new_user':new_user
#             }
#             return render(request,'accaunt/register_done.html',context)
#         else:
#             # Handle the case when the form is not valid
#             return HttpResponseBadRequest("Form data is not valid.")
#     else:
#         user_form=UserRegistrationForm()
#         context={
#             'user_form':user_form
#         }
#         return render(request,'accaunt/register.html',context)
# def user_register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(
#                 user_form.cleaned_data['password']
#             )
#             new_user.save()
#             Profile.objects.create(user=new_user)
#             context = {
#                 'new_user': new_user
#             }
#             return render(request, 'accaunt/register_done.html', context)
#         else:
#             # Handle the case when the form is not valid
#             return HttpResponseBadRequest("Form data is not valid.")
#     else:
#         user_form = UserRegistrationForm()
#         context = {
#             'user_form': user_form
#         }
#         return render(request, 'accaunt/register.html', context)
def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)



            context = {
                'new_user': new_user
            }    # Send email confirmation asynchronously using Celery
            subject = 'Account Registration Confirmation'
            message = f'Hello {new_user.username}, your account has been successfully registered.'
            recipient_list = [new_user.email]
            send_email.delay(subject, message, recipient_list)
            return render(request, 'accaunt/register_done.html', context)
        else:
            # Handle the case when the form is not valid
            return HttpResponseBadRequest("Form data is not valid.")
    else:
        user_form = UserRegistrationForm()
        context = {
            'user_form': user_form
        }
        return render(request, 'accaunt/register.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accaunt/register.html'

@login_required
def edit_user(request):
    if request.method== 'POST':
        user_form=UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,
                                     data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    return render(request,'accaunt/profile_edit.html',{'user_form':user_form,'profile_form':profile_form})

class EditUserView(LoginRequiredMixin,View):
    def get(self,request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(request, 'accaunt/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
    def post(self,request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')


        