from django import forms
from django.core.mail import send_mail
from django.conf import settings


class ContactForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    message = forms.CharField(
        label='お問い合わせ内容',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def send_email(self):

        subject = '[WHT]' + self.cleaned_data['email'] + '様からのお問い合わせ'
        message = self.cleaned_data['message']
        from_email = settings.EMAIL_HOST_USER
        to = [settings.EMAIL_HOST_USER]

        send_mail(subject, message, from_email, to)