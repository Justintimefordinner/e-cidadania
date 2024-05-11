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
This module contains all the space related forms, including the forms for
documents, meetings and entities. Most of the forms are directly generated
from the data models.
"""

from django.forms import ModelForm, ValidationError

from core.spaces.models import Space, Document, Event, Entity

class SpaceForm(ModelForm):
    class Meta:
        model = Space

    def clean_image_file(self, file_field):
        valid_image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        image_file = self.cleaned_data[file_field]
        for extension in valid_image_extensions:
            if image_file.name.endswith(''.join(['.', extension])):
                return image_file
        raise ValidationError("Invalid file extension")

    def clean_logo(self):
        return self.clean_image_file('logo')

    def clean_banner(self):
        return self.clean_image_file('banner')

class DocForm(ModelForm):
    class Meta:
        model = Document

class RoleForm(ModelForm):
    class Meta:
        model = Space
        exclude = ('name', 'url', 'date', 'description', 'logo', 'banner',
            'author', 'mod_debate', 'mod_proposals', 'mod_news', 'mod_cal',
            'mod_docs', 'mod_voting', 'public')

class EventForm(ModelForm):
    class Meta:
        model = Event