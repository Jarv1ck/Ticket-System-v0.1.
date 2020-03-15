from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate

from .forms import UserCreateForm
'''
Rebuild to CLASS BASED VIEWS
'''


def user_creation(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pswd = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = authenticate(username=username, password=pswd,
                                email=email, first_name=first_name,
                                last_name=last_name)

        return HttpResponseRedirect(reverse('tickets:main'))
    else:
        form = UserCreateForm()
        return render(request, 'accounts/create.html', {'form': form})



