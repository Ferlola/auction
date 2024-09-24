import datetime

from django import forms
from django.utils import timezone

from src.adminauction.models import UserPermission
from src.articles.models import Article
from src.articles.models import ImageUpload


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "article",
            "description",
            "location",
            "category",
            "subcategory",
            "reserved",
            "from_date",
            "date_time",
        ]

        labels = {
            "reserved": "Reserved price?",
            "description": "Description (max=255chr)",
            "location": "Location, city..etc..",
            "category": "Select category",
            "subcategory": "Select subcategory",
            "from_date": "From date?",
            "date_time": "Until what date and time?",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if UserPermission.objects.filter(choose_date_time=True):
            self.fields["from_date"].widget.attrs["show"] = True
            self.fields["date_time"].widget.attrs["show"] = True
        else:
            del self.fields["from_date"]
            del self.fields["date_time"]

        if self.instance and self.instance.article:
            self.fields["article"].widget.attrs["readonly"] = True
            self.fields["article"].label = ""

        self.fields["article"].widget.attrs.update(
            {
                "class": "form-control",
                "type": "text",
                "style": "width: 400px;",
            },
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "type": "text",
                "style": "width: 600px;",
            },
        )
        self.fields["location"].widget.attrs.update(
            {
                "class": "form-control",
                "type": "text",
                "style": "width: 600px;",
            },
        )
        self.fields["category"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "width: 200px;",
            },
        )
        self.fields["subcategory"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "width: 200px;",
            },
        )
        self.fields["reserved"].widget = forms.widgets.NumberInput(
            attrs={
                "class": "form-control",
                "min": 0,
                "style": "width: 100px;",
            },
        )
        if UserPermission.objects.filter(choose_date_time=True):
            self.fields["from_date"].widget = forms.widgets.DateInput(
                attrs={
                    "class": "form-control",  # timepicker
                    "style": "width: 190px;",
                    "type": "date",
                },
            )
            self.fields["date_time"].widget = forms.widgets.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "style": "width: 220px",
                    "type": "datetime-local",
                },
            )

    def clean_from_date(self):
        from_date = self.cleaned_data.get("from_date")
        today = datetime.datetime.now(tz=datetime.UTC).date()
        if from_date is None:
            msg = "Please select the start date"
            raise forms.ValidationError(msg)

        if from_date < today:
            msg = "The start date cannot be before today"
            raise forms.ValidationError(msg)
        return from_date

    def clean_date_time(self):
        from_date = self.cleaned_data.get("from_date")
        date_time = self.cleaned_data.get("date_time")
        if from_date is None:
            msg = "Please select the start date"
            raise forms.ValidationError(msg)
        if date_time is None:
            msg = "Please select date and time to finish the auction"
            raise forms.ValidationError(msg)
        time_now = timezone.now()
        date_time_ = date_time.date()

        if from_date:
            if from_date > date_time_:
                msg = "The end auction cannot be before the start"
                raise forms.ValidationError(msg)
            if date_time < time_now:
                msg = "The hour cannot have passed"
                raise forms.ValidationError(msg)
        return date_time


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ["image"]
        labels = {"image": "Upload image"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["image"].widget = forms.FileInput()
