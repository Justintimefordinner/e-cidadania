# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Clione Software
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
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

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from e_cidadania import settings


def index_view(request):

    """
    Main view for the index page. It's separated from the urls.py file
    because using direct_to_template in urls.py doesn't refresh the content
    (it's loaded only once).
    """
    extra_context = {
        'version': settings.__version__,
        'status': settings.__status__,
        'debug_mode': settings.DEBUG,
        #'cache_timeout': 500,
    }

    if not request.user.is_authenticated:
        messages.warning(request, _("Hi! It seems that it's your first time \
        here. Maybe you want to <a href=\"/accounts/register\">register</a> \
        or <a href=\"/accounts/login/\">login</a> if you have an account."))

        return render(request, 'site_index.html', extra_context)
    else:
        return redirect(reverse_lazy('profile_overview'))