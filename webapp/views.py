# -*- coding: utf-8 -*-
import json
import urllib
import urlparse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from doyouhavetime import settings
from webapp import models
from webapp.models import Times, Plans

dates = ['월', '화', '수', '목', '금', '토', '일']
loop_times = [i for i in range(9, 22)]


def login_required_ajax(function=None, redirect_field_name=None):
    """
    Just make sure the user is authenticated to access a certain ajax view

    Otherwise return a HttpResponse 401 - authentication required
    instead of the 302 redirect of the original Django decorator
    """

    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(status=401)

        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


@ensure_csrf_cookie
def home(request):
    ctx = Context({
        'result': False,
        'dates': dates,
        'loop_times': loop_times
    })
    return render(request, 'index.html', ctx)


@login_required_ajax
def done(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        try:
            data = ""
            for i in json_data['times']:
                data += json.dumps(i, ensure_ascii=False).encode('utf8').replace("\"", "") + " "
            user = request.user
            Times(times=data, user=user, parent_plan=Plans.objects.first()).save()
        except KeyError:
            HttpResponseServerError("Malformed data!")
    return HttpResponse("Got json data")


@login_required_ajax
def result(request):
    times_result = []
    times = Plans.objects.first().times_set.all()
    for i in times:
        for j in i.times.split():
            times_result.append(j)
    times_result = list(set(times_result))
    return HttpResponse(json.dumps(times_result))


def login(request):
    error = None

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.GET:
        if 'code' in request.GET:
            args = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                'client_secret': settings.FACEBOOK_API_SECRET,
                'code': request.GET['code'],
            }
            url = 'https://graph.facebook.com/oauth/access_token?' + \
                  urllib.urlencode(args)
            response = urlparse.parse_qs(urllib.urlopen(url).read())

            access_token = response['access_token'][0]
            expires = response['expires'][0]

            facebook_session = models.FacebookSession.objects.get_or_create(access_token=access_token, )[0]
            facebook_session.expires = expires
            facebook_session.save()

            user = auth.authenticate(token=access_token)
            if user:
                if user.is_active:
                    auth.login(request, user)

                    return HttpResponseRedirect('/')
                else:
                    error = 'AUTH_DISABLED'
            else:
                error = 'AUTH_FAILED'
        elif 'error_reason' in request.GET:
            error = 'AUTH_DENIED'

    template_context = {'settings': settings, 'error': error}
    print error
    return render_to_response('login.html', template_context, context_instance=RequestContext(request))