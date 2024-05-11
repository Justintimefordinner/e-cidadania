from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", [])
        self.max_upload_size = kwargs.pop("max_upload_size", None)

        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
        except AttributeError:
            pass
        else:
            if content_type not in self.content_types:
                raise forms.ValidationError(_('Filetype not supported.'))
            if file.size > self.max_upload_size:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s.') % (filesizeformat(self.max_upload_size), filesizeformat(file.size)))

        return data