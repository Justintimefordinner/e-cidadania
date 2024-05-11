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
This file contains all the URLs that e_cidadania will inherit when the user
access to '/spaces/'.
"""
from django.urls import path, re_path, include

from core.spaces.views.spaces import ViewSpaceIndex, ListSpaces, \
    DeleteSpace
from core.spaces.views.documents import ListDocs, DeleteDocument, \
    AddDocument, EditDocument
from core.spaces.views.events import ListEvents, DeleteEvent, ViewEvent, \
    AddEvent, EditEvent
from core.spaces.views.rss import SpaceFeed
from core.spaces.views.intent import ValidateIntent
from core.spaces.views.news import ListPosts, YearlyPosts, MonthlyPosts, \
    RedirectArchive
from core.spaces.url_names import *

# NOTICE: Don't change the order of urlpatterns or it will probably break.

urlpatterns = [

    # RSS Feed
    path('<str:space_url>/rss/', SpaceFeed.as_view(), name=SPACE_FEED),

    # News
    path('<str:space_url>/news/',
        include('apps.ecidadania.news.urls')),

    # Proposals
    path('<str:space_url>/proposal/',
        include('apps.ecidadania.proposals.urls')),

    # Calendar
    path('<str:space_url>/calendar/',
        include('apps.ecidadania.cal.urls')),

    # Debates
    path('<str:space_url>/debate/',
        include('apps.ecidadania.debate.urls')),

    # Votes
    path('<str:space_url>/voting/',
        include('apps.ecidadania.voting.urls')),

    # Document URLs
    path('<str:space_url>/docs/add/', AddDocument.as_view(),
        name=DOCUMENT_ADD),

    path('<str:space_url>/docs/<int:doc_id>/edit/',
        EditDocument.as_view(), name=DOCUMENT_EDIT),

    path('<str:space_url>/docs/<int:doc_id>/delete/',
        DeleteDocument.as_view(), name=DOCUMENT_DELETE),

    path('<str:space_url>/docs/', ListDocs.as_view(),
        name=DOCUMENT_LIST),

    # Event URLs
    path('<str:space_url>/event/add/', AddEvent.as_view(),
        name=EVENT_ADD),

    path('<str:space_url>/event/<int:event_id>/edit/',
        EditEvent.as_view(), name=EVENT_EDIT),

    path('<str:space_url>/event/<int:event_id>/delete/',
        DeleteEvent.as_view(), name=EVENT_DELETE),

    path('<str:space_url>/event/<int:event_id>/',
        ViewEvent.as_view(), name=EVENT_VIEW),

    path('<str:space_url>/event/', ListEvents.as_view(),
        name=EVENT_LIST),

    # Intent URLs
    path('<str:space_url>/intent/',
        'core.spaces.views.intent.add_intent', name=INTENT_ADD),

    path('<str:space_url>/intent/approve/<str:token>/',
        ValidateIntent.as_view(), name=INTENT_VALIDATE),

    # Spaces URLs
    path('<str:space_url>/edit/',
        'core.spaces.views.spaces.edit_space', name=SPACE_EDIT),

    path('<str:space_url>/delete/', DeleteSpace.as_view(),
        name=SPACE_DELETE),

    path('<str:space_url>/news/', RedirectArchive.as_view(),
        name=SPACE_NEWS),

    path('<str:space_url>/news/archive/', ListPosts.as_view(),
        name=NEWS_ARCHIVE),

    path('<str:space_url>/news/archive/<int:year>/',
        YearlyPosts.as_view(), name=NEWS_YEAR),

    path('<str:space_url>/news/archive/<int:year>/<str:month>/',
        MonthlyPosts.as_view(), name=NEWS_MONTH),

    path('add/', 'core.spaces.views.spaces.create_space',
        name=SPACE_ADD),

    path('', ListSpaces.as_view(), name=SPACE_LIST),

    # path(_(r'^go/'), GoToSpace.as_view(), name=GOTO_SPACE),

    path('<str:space_url>/roles/', 'core.spaces.views.spaces.edit_roles',
        name=EDIT_ROLES),

    path('<str:space_url>/search_user/',
        'core.spaces.views.spaces.search_user', name=SEARCH_USER),

    path('<str:space_url>/', ViewSpaceIndex.as_view(),
        name=SPACE_INDEX),

]