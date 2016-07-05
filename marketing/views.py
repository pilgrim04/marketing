# -*- coding: utf-8 -*-
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.generic import FormView, RedirectView, View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from django.shortcuts import render
import xlsxwriter


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        # TODO: do redirect to cabinet if user already logged in
        # if self.request.user.is_authenticated():
        #     return HttpResponseRedirect('/cabinet')
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect('/cabinet')

    def form_invalid(self, form):
        context = super(LoginView, self).form_invalid(form)

        return context


class LogoutView(TemplateView):
    template_name = 'logout.html'

    def get(self, *args, **kwargs):
        auth_logout(self.request)
        return super(LogoutView, self).get(*args, **kwargs)


class EditProfileView(TemplateView):
    template_name = 'edit.html'

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        return context


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(data['login'],
                                        data['email'],
                                        data['password'],
                                        first_name=data['first_name'],
                                        last_name=data['last_name'])
        user.save()

        return HttpResponseRedirect('/cabinet')


class CabinetView(TemplateView):
    template_name = 'cabinet.html'
    # TODO: настроить декоратор

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated() or self.request.user.is_anonymous():
            # return HttpResponseRedirect(reverse('login'))
            raise ValueError('You are not log in. Please do it.')
        context = super(CabinetView, self).get_context_data(**kwargs)
        if self.request.user.first_name:
            context['current_user'] = self.request.user.first_name
        else:
            context['current_user'] = self.request.user

        return context

