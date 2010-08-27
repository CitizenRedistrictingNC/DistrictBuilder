# Copyright 2010 Micah Altman, Michael McDonald
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.utils import simplejson as json

# for proxy
import urllib2
import cgi
import sys, os

# for password reminders
import smtplib
from random import choice

def index(request):
    """Generate the index page for the application. The
    index template contains a login button, a register
    button, and an anonymous button, all of which interact
    with django's authentication system."""
    return render_to_response('index.html', { })

def userregister(request):
    """The view to process when a client attempts to register.
    A user can log in if their username is unique, and their
    password is not empty. An email address is optional. This
    view returns a JSON nugget, with a 'success' property.

    If registration was successful, the JSON nugget also contains
    a 'redirect' property.

    If registration was unsuccessful, the JSON script also contains
    a 'message' property, describing why the registration failed.
    """
    username = request.POST.get('newusername', None)
    password = request.POST.get('newpassword1', None)
    email = request.POST.get('email', None)
    fname = request.POST.get('firstname', None)
    lname = request.POST.get('lastname', None)
    hint = request.POST.get('passwordhint', None)
    org = request.POST.get('organization', None)
    anonymous = False
    status = { 'success':False }
    if username != '' and password != '':
        anonymous = (username == 'anonymous' and password == 'anonymous')

        name_exists = User.objects.filter(username__exact=username)
        if name_exists and not anonymous:
            status['message'] ='name exists'
            return HttpResponse(json.dumps(status), mimetype='application/json')

        email_exists = email != '' and User.objects.filter(email__exact = email)
        if email_exists and not anonymous:
            status['message'] ='email exists'
            return HttpResponse(json.dumps(status), mimetype='application/json')

        if not anonymous:
            try:
                User.objects.create_user(username, email, password)
            except Exception as error:
                status['message'] = 'Sorry, we weren\'t able to create your account.'
                return HttpResponse(json.dumps(status), mimetype='application/json')

        # authenticate the user, and add additional registration info
        user = authenticate(username=username, password=password)

        if not anonymous:
            user.first_name = fname
            user.last_name = lname
            user.save()

            profile = user.get_profile()
            profile.organization = org
            profile.pass_hint = hint
            profile.save()

        login( request, user )
        status['success'] = True
        status['redirect'] = '/districtmapping/plan/0/view'
        return HttpResponse(json.dumps(status), mimetype='application/json')
    else:
        status['message'] = 'Username cannot be empty.'
        return HttpResponse(json.dumps(status), mimetype='application/json')

def userlogout(request):
    """Log out a client from the application. This uses django's
    authentication system to clear the session, etc. The view will
    redirect the user to the index page after logging out."""
    logout(request)
    return HttpResponseRedirect('/')

def emailpassword(user):
    """Send a user an email with a new, auto-generated password.
    We cannot decrypt the current password stored with the user record,
    so create a new one, and send it to the user."""

    tpl = """To: %s
From: "%s" <%s>
Subject: Your Password Reset Request

Hello %s,

You requested a new password for the Public Mapping Project. Sorry for the
inconvenience!  This is your new password: "%s"

Thank you for using the Public Mapping Project.

Happy Redistricting!
The Public Mapping Team
"""
    admin = settings.ADMINS[0][0]
    sender = settings.ADMINS[0][1]

    newpw = ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+') for i in range(8)])

    try:
        smtp = smtplib.SMTP( settings.MAIL_SERVER, settings.MAIL_PORT )
        smtp.ehlo()
        if settings.MAIL_PORT == '587':
            smtp.starttls()
        if settings.MAIL_USERNAME != '' and settings.MAIL_PASSWORD != '':
            smtp.login( settings.MAIL_USERNAME, settings.MAIL_PASSWORD )

        msg = tpl % (user.email, admin, sender, user.username, newpw)
        smtp.sendmail( sender, user.email, msg )
        smtp.quit()

        user.set_password(newpw)
        user.save()
        return True
    except:
        return False

@cache_control(no_cache=True)
def forgotpassword(request):
    """If someone has forgotten their password, provide a facility
    for retrieving it."""
    status = {'success':False}
    if 'username' in request.REQUEST and not request.REQUEST['username'] == '':
        username = request.REQUEST['username']
        try:
            user = User.objects.get(username__exact=username)
            status['success'] = True
            status['mode'] = 'hinting'
            status['hint'] = user.get_profile().pass_hint
        except:
            status['field'] = 'username'
            status['message'] = 'Invalid username. Please try again.'
    elif 'email' in request.REQUEST and not request.REQUEST['email'] == '':
        email = request.REQUEST['email']
        try:
            user = User.objects.get(email__exact=email)
            status['mode'] = 'sending'
            status['success'] = emailpassword(user)
        except:
            status['field'] = 'email'
            status['message'] = 'Invalid email address. Please try again.'
    else:
        status['field'] = 'both'
        status['message'] = 'Missing username or email.'

    return HttpResponse(json.dumps(status), mimetype='application/json')

@login_required
def mapping(request):
    """The view for the mapping page. The mapping page requires
    a valid user, and as such, is decorated with login_required."""
    return render_to_response('mapping.html', 
        { 'mapserver': settings.MAP_SERVER })

@login_required
@cache_control(no_cache=True)
def proxy(request):
    """A proxy view that proxies all requests to the map server through
    this django app. This is required for WFS requests and queries."""
    url = request.GET['url']

    host = url.split('/')[2]
    if host != settings.MAP_SERVER:
        raise Http404

    if request.method == 'POST':
        rsp = urllib2.urlopen( urllib2.Request(
            url, 
            request.raw_post_data,
            {'Content-Type': request.META['CONTENT_TYPE'] }
        ))
    else:
        rsp = urllib2.urlopen(url)

    httprsp = HttpResponse( rsp.read() )
    if rsp.info().has_key('Content-Type'):
        httprsp['Content-Type'] = rsp.info()['Content-Type']
    else:
        httprsp['Content-Type'] = 'text/plain'

    rsp.close()

    return httprsp

