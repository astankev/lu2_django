from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from user.models import User
from django.views.generic import FormView, View, ListView
from user.forms import UserForm


class UserListView(ListView):

    model = User
    template_name = 'user_list.html'

class AddUserView(FormView):

    form_class = UserForm
    template_name = 'add_user.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        form.save()

        response = super().form_valid(form)
        return response


def get_user(request, user_id):

    user = User.objects.get(pk=user_id)

    context = {
        'user': user,
    }

    return render(
        template_name='user.html',
        request=request,
        context=context,

    )


def delete_user(request, user_id):

    user = User.objects.get(pk=user_id)
    user.delete()

    return HttpResponse(f'Deleted {user.username}')


def edit_user(request, user_id):

    user = User.objects.get(id=user_id)

    if request.method == 'POST':

        username = request.POST['name']
        email = request.POST['email']

        if len(username) != 0:
            user.username = username

        if len(email) != 0:
            user.email = email

        user.save()

        context = {
            'user': user,
        }

        return render(
            template_name='user.html',
            request=request,
            context=context,

        )

    return render(
        template_name='form.html',
        request=request
    )