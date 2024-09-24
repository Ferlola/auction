from django import forms

from src.bids.models import BidsHistory


class BidForm(forms.ModelForm):
    class Meta:
        model = BidsHistory
        fields = ["bids"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["bids"].widget = forms.widgets.NumberInput(
            attrs={
                "class": "form-control",
                "min": 0,
                "type": "number",
                "style": "width: 200px;",
            },
        )
