from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, label="Your Name")
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 6}), label="Message")
    recaptcha_token = forms.CharField(required=False, widget=forms.HiddenInput)