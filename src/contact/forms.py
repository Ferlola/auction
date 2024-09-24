from django import forms


class ContactForm(forms.Form):
    category = forms.CharField()
    message = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].label = "category"
        self.fields["message"].label = "message"


class AskSellerForm(forms.Form):
    message = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].label = "message"
