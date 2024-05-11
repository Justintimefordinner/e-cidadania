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

from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .allowed_types import ALLOWED_CONTENT_TYPES
#from .fields import StdImageField
from .file_validation import ContentTypeRestrictedFileField


class Space(models.Model):
    """
    Spaces model. This model stores a "space" or "place" also known as a
    participative process in reality. Every place has a minimum set of
    settings for customization.

    There are three main permission roles in every space: administrator
    (admins), moderators (mods) and regular users (users).
    """
    name = models.CharField(_('Name'), max_length=250, unique=True,
                            help_text=_('The name of the space. Max: 250 characters.'))
    url = models.SlugField(_('URL'), max_length=100, unique=True,
                           help_text=_('The URL of the space. This will be the accessible URL.'))
    description = models.TextField(_('Description'), default=_('Write here your description.'),
                                   help_text=_('The description of the space.'))
    pub_date = models.DateTimeField(_('Date of creation'), auto_now_add=True,
                                    help_text=_('The date the space was created.'))
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                               verbose_name=_('Space creator'), related_name='spaces',
                               help_text=_('The user that will be marked as creator of the space.'))
    logo = models.ImageField(upload_to='spaces/logos', max_length=250, blank=True, null=True,
                             help_text=_('The logo of the space. Valid extensions are jpg, jpeg, png and gif.'))
    banner = models.ImageField(upload_to='spaces/banners', max_length=250, blank=True, null=True,
                               help_text=_('The banner of the space. Valid extensions are jpg, jpeg, png and gif.'))
    public = models.BooleanField(_('Public space'), default=False,
                                 help_text=_("If checked, this will make the space visible to everyone, but registration will be necessary to participate."))

    # Modules
    MODULE_CHOICES = [
        (False, _('Disabled')),
        (True, _('Enabled')),
    ]
    mod_debate = models.BooleanField(_('Debate'), choices=MODULE_CHOICES, default=False,
                                     help_text=_('Enable or disable the debate module.'))
    mod_proposals = models.BooleanField(_('Proposals'), choices=MODULE_CHOICES, default=False,
                                        help_text=_('Enable or disable the proposals module.'))
    mod_news = models.BooleanField(_('News'), choices=MODULE_CHOICES, default=False,
                                   help_text=_('Enable or disable the news module.'))
    mod_cal = models.BooleanField(_('Calendar'), choices=MODULE_CHOICES, default=False,
                                  help_text=_('Enable or disable the calendar module.'))
    mod_docs = models.BooleanField(_('Documents'), choices=MODULE_CHOICES, default=False,
                                   help_text=_('Enable or disable the documents module.'))
    mod_voting = models.BooleanField(_('Voting'), choices=MODULE_CHOICES, default=False,
                                     help_text=_('Enable or disable the voting module.'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Space')
        verbose_name_plural = _('Spaces')
        get_latest_by = 'pub_date'
        permissions = (
            ('view_space', 'Can view this space.'),
            ('admin_space', 'Can administrate this space.'),
            ('mod_space', 'Can moderate this space.')
        )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Space: {self.name} ({self.url})>"

    def get_absolute_url(self):
        return reverse('space-index', args=[str(self.url)])


class Entity(models.Model):
    """
    This model stores the name of the entities responsible for the creation
    of the space or supporting it.
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    website = models.URLField(_('Website'), max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='spaces/logos', verbose_name=_('Logo'), blank=True, null=True)
    space = models.ForeignKey(Space, blank=True, null=True, on_delete=models.CASCADE, related_name='entities')

    class Meta:
        ordering = ['name']
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')

    def __str__(self):
        return self.name

class Document(models.Model):

    """
    This models stores documents for the space, like a document repository,
    There is no restriction in what a user can upload to the space.

    :methods: get_file_ext, get_file_size
    """
    title = models.CharField(_('Document title'), max_length=100,
        help_text=_('Max: 100 characters'))
    space = models.ForeignKey(Space, blank=True, null=True,
        help_text=_('Change the space to whom belongs this document'))
    docfile = ContentTypeRestrictedFileField(_('File'),
        upload_to='spaces/documents/%Y/%m/%d',
        content_types=ALLOWED_CONTENT_TYPES,
        max_upload_size=26214400,
        help_text=_('Permitted file types: DOC, DOCX, PPT, ODT, ODF, ODP, \
            PDF, RST, TXT.'))
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name=_('Author'), blank=True,
        null=True, help_text=_('Change the user that will figure as the \
        author'))

    def get_file_ext(self):
        filename, extension = os.path.splitext(self.docfile.name)
        return extension[1:].upper()

    def get_file_size(self):
        size = self.docfile.size
        units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
        for unit in units:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

    class Meta:
        ordering = ['pub_date']
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        get_latest_by = 'pub_date'

    def get_absolute_url(self):
        return reverse('spaces:docs', args=[self.space.url, self.id])

class Event(models.Model):

    """
    Meeting data model. Every space (process) has N meetings. This will
    keep record of the assistants, meeting name, etc.
    """
    title = models.CharField(_('Event name'), max_length=250,
        help_text="Max: 250 characters")
    space = models.ForeignKey(Space, blank=True, null=True)
    user = models.ManyToManyField(User, verbose_name=_('Users'),
        help_text=_('List of the users that will assist or assisted to the \
        event.'))
    pub_date = models.DateTimeField(auto_now_add=True)
    event_author = models.ForeignKey(User, verbose_name=_('Created by'),
        blank=True, null=True, related_name='meeting_author',
        help_text=_('Select the user that will be designated as author.'))
    event_date = models.DateTimeField(verbose_name=_('Event date'),
        help_text=_('Select the date where the event is celebrated.'))
    description = models.TextField(_('Description'), blank=True, null=True)
    location = models.TextField(_('Location'), blank=True, null=True)
    latitude = models.DecimalField(_('Latitude'), blank=True, null=True,
        max_digits=17, decimal_places=15, help_text=_('Specify it in decimal'))
    longitude = models.DecimalField(_('Longitude'), blank=True, null=True,
        max_digits=17, decimal_places=15, help_text=_('Specify it in decimal'))

    def is_due(self):
        if self.event_date < timezone.now():
            return True
        else:
            return False

    class Meta:
        ordering = ['event_date']
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        get_latest_by = 'event_date'
        permissions = (
            ('view_event', 'Can view this event'),
            ('admin_event', 'Can administrate this event'),
            ('mod_event', 'Can moderate this event'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view-event', kwargs={
            'space_url': self.space.url,
            'event_id': str(self.id)
        })


class Intent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    requested_on = models.DateTimeField(auto_now_add=True)

    def get_approve_url(self):
        site = Site.objects.get_current()
        return "http://{}{}intent/approve/{}".format(site.domain, reverse('space-detail', args=[self.space.id]), self.token)