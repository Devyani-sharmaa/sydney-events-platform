from django import forms

class TicketForm(forms.Form):
    email = forms.EmailField(label="Your Email")
    consent = forms.BooleanField(label="I agree to receive updates", required=True)
