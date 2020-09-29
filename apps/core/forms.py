from django import forms

from apps.core.models import ContactUs
from apps.core.utils import phone_formatting
from apps.core.validators import name_validator


class PhoneFormMixin(forms.Form):
    phone = forms.CharField()

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = phone_formatting(phone)
        if len(phone) != 12:
            raise forms.ValidationError('length != 12')
        return phone


class ContactUsModelForm(forms.ModelForm, PhoneFormMixin):
    name = forms.CharField(
        max_length=10,
        label='first name',
        required=True,
        validators=[name_validator]
    )
    message = forms.CharField(widget=forms.Textarea({'cols': 20, 'rows': 2}))

    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'phone', 'subject', 'message')


    def clean_name(self):
        name = self.cleaned_data.get('name')

        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) < 10:
            raise forms.ValidationError(
                '%(email)s < 10',
                params={'email': email}
            )
        return email
