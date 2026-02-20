from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from mailing.models import Dispatch


class StyleFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                # field.widget.attrs.update({'class': 'form-check'})
                field.widget.attrs["class"] = "form-check-input"
                # field.widget.attrs['input type'] = 'checkbox'
            else:
                field.widget.attrs["class"] = "form-control"


class DispatchForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Dispatch
        exclude = (
            "owner",
            "is_published",
        )
