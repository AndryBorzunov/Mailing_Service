import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from mailing.models import Dispatch, RecipientMail, Message


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
            "status",
        )

    def clean_start_time(self):
        start_t = self.cleaned_data.get("start_time")
        current_time = datetime.datetime.now().timestamp()
        if start_t.timestamp() < current_time:
            raise ValidationError("Время начала рассылки не может быть в прошлом")
        return start_t

    def clean_end_time(self):
        end_t = self.cleaned_data.get("end_time")
        current_time = datetime.datetime.now().timestamp()
        if end_t.timestamp() < current_time:
            raise ValidationError("Время окончания рассылки не может быть в прошлом")
        return end_t

    def clean(self):
        cleaned_data = super().clean()
        start_t = cleaned_data.get("start_time")
        end_t = cleaned_data.get("end_time")

        if start_t is None:
            self.add_error("start_time", "Error")
        elif end_t is None:
            self.add_error("end_time", "Error")
        else:
            if end_t.timestamp() < start_t.timestamp():
                self.add_error(
                    "end_time",
                    "Время начала рассылки должно быть раньше времени окончания",
                )
        return self.cleaned_data


class DispatchModeratorForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Dispatch
        fields = ("is_active",)


class RecipientMailForm(StyleFormMixin, ModelForm):

    class Meta:
        model = RecipientMail
        exclude = ("owner",)


class MessageForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Message
        exclude = ("owner",)
