from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _


class MyAuthForm(AuthenticationForm):
    username = forms.CharField(
        label="RTAF-Mail",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "อีเมล ทอ. (ไม่ต้องใส่ @rtaf.mi.th)",
        })
    )

    password = forms.CharField(
        label="OTP (ดูใน Superapp)",
        widget=forms.PasswordInput(attrs={
            "class": "form-control auth-pass-inputgroup",
            "placeholder": "กรอกรหัส OTP 6 หลัก",
            "autocomplete": "one-time-code",
            "inputmode": "numeric",
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip().lower()

        DOMAIN = "@rtaf.mi.th"

        if username.endswith(DOMAIN):
            username = username[:-len(DOMAIN)]

        return username