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

"""
Main URLs for the e-cidadania platform.
"""

from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from core.views.index import index_view
from core.views.invite import invite
from core.views.explore import explore

admin.autodiscover()

# We put here the dictionary with all the packages for translating JavaScript code
# Please refer to https://docs.djangoproject.com/en/dev/topics/i18n/internationalization/#specifying-translation-strings-in-javascript-code
js_info_dict = {
    'packages': ('apps.ecidadania.debate',),
}

urlpatterns = [
    # i18n switcher
    path('i18n/', include('django.conf.urls.i18n')),

    # Django administration
    path('admin/', admin.site.urls),

    # Index
    path('', index_view, name='site-index'),

    # User accounts
    path('accounts/', include('apps.thirdparty.userprofile.urls')),

    # REST API
    path('api/', include('apps.ecidadania.api.urls')),

    # Spaces
    path('spaces/', include('core.spaces.urls')),

    # Invitations
    path('invite/', invite, name='invite'),

    # Explore
    path('explore/', explore, name='explore'),

    # This urls is for the django comments system
    path('comments/', include('django.contrib.comments.urls')),

    path('jsi18n/', 'django.views.i18n.javascript_catalog', js_info_dict),

    # For smart_selects app
    path('chaining/', include('apps.thirdparty.smart_selects.urls')),

    # This url is for the access to static pages. I hope this doesn't collide
    # with the index view
    path('<slug:slug>/', include('apps.ecidadania.staticpages.urls')),
]

if settings.DEBUG:
    # Serve static files
    urlpatterns += staticfiles_urlpatterns()
    # Serve uploaded files
    urlpatterns += [
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    ]