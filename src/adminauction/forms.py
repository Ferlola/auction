import datetime

from django import forms
from django.utils import timezone

from src.adminauction.models import FeeArticle
from src.adminauction.models import SetBidArticle
from src.adminauction.models import UserPermission
from src.articles.models import Article
from src.categories.models import Category
from src.categories.models import Subcategory


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
            "description": "Description (max=255chs)",
            "location": "Location, city..etc..",
            "category": "Select category",
            "subcategory": "Select subcategory",
            "from_date": "From date?",
            "date_time": "Until what date and time?",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                "type": "number",
                "style": "width: 100px;",
            },
        )
        self.fields["from_date"].widget = forms.widgets.DateInput(
            attrs={
                "class": "form-control",
                "style": "width: 190px;",
                "type": "date",
            },
        )
        self.fields["date_time"].widget = forms.widgets.DateTimeInput(
            attrs={
                "class": "form-control",
                "style": "width: 220px;",
                "type": "datetime-local",
            },
        )

    def clean_from_date(self):
        from_date = self.cleaned_data.get("from_date")
        today = datetime.datetime.now(tz=datetime.UTC).date()
        if from_date < today:
            msg = "The start date cannot be before today"
            raise forms.ValidationError(msg)
        return from_date

    def clean_date_time(self):
        from_date = self.cleaned_data.get("from_date")
        date_time = self.cleaned_data.get("date_time")
        if not date_time:
            msg = "Please select date and time"
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


class DateTimeForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["from_date", "date_time"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["from_date"].widget = forms.widgets.DateInput(
            attrs={
                "class": "form-control",
                "style": "width: 190px;",
                "type": "date",
            },
        )
        self.fields["date_time"].widget = forms.widgets.DateTimeInput(
            attrs={
                "class": "form-control",
                "style": "width: 220px;",
                "type": "datetime-local",
            },
        )


class PermissionForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        fields = (
            "article_update",
            "choose_date_time",
            "total_images",
            "theme",
            "site_name",
            "domain",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["theme"].widget = forms.RadioSelect()

        self.fields["article_update"].widget = forms.CheckboxInput()

        self.fields["choose_date_time"].widget = forms.CheckboxInput()

        self.fields["total_images"].widget = forms.widgets.NumberInput(
            attrs={
                "class": "form-control",
                "min": 0,
                "type": "number",
                "style": "width: 100px;",
            },
        )
        self.fields["site_name"].widget = forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "style": "width: 100px;",
            },
        )
        self.fields["domain"].widget = forms.widgets.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "style": "width: 100px;",
            },
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        labels = {"name": "Category Name"}
        widgets = {"name": forms.TextInput(attrs={"maxlength": 100})}


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ("category", "name")
        labels = {"category": "Please select category", "name": "Subcategory name"}
        widgets = {
            "category": forms.Select(attrs={"maxlength": 100}),
            "name": forms.TextInput(attrs={"maxlength": 100}),
        }


class FeeForm(forms.ModelForm):
    class Meta:
        model = FeeArticle
        fields = ("fee",)
        widgets = {
            "fee": forms.NumberInput(
                attrs={
                    "step": 0.01,
                    "min": 0.00,
                    "max": 99.99,
                },
            ),
        }


class SetBidarticleForm(forms.ModelForm):
    set_bid = forms.ChoiceField(
        choices=SetBidArticle.BID_CHOICES,
        widget=forms.RadioSelect(),
    )

    class Meta:
        model = SetBidArticle
        fields = ["set_bid", "bid_amount", "publish"]
        labels = {"bid_amount": "", "publish": "Publish"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["bid_amount"].widget = forms.widgets.NumberInput(
            attrs={
                "class": "form-control",
                "min": 0,
                "type": "number",
                "style": "width: 200px;",
            },
        )

    def clean_bid_amount(self):
        set_bid = self.cleaned_data.get("set_bid")
        bid_amount = self.cleaned_data.get("bid_amount")
        if set_bid == "2" and not bid_amount:
            msg = "Please enter bid amount"
            raise forms.ValidationError(msg)
        return bid_amount


class CrontabWeeklyForm(forms.Form):
    CHOICES = [
        ("1", "Monday"),
        ("2", "Tuesday"),
        ("3", "Wednesday"),
        ("4", "Thursday"),
        ("5", "Friday"),
        ("6", "Saturday"),
        ("0", "Sunday"),
    ]
    day_of_week = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    hour = forms.IntegerField()
    hour.widget.attrs.update(
        {
            "class": "form-control",
            "min": 0,
            "max": 23,
            "type": "number",
            "style": "width: 100px;",
            "placeholder": "0 - 23",
        },
    )
    minute = forms.IntegerField()
    minute.widget.attrs.update(
        {
            "class": "form-control",
            "min": 0,
            "max": 59,
            "type": "number",
            "style": "width: 100px;",
            "placeholder": "0 - 59",
        },
    )
    task_name = forms.CharField(max_length=50)
    task_name.widget.attrs.update(
        {
            "class": "form-control",
            "type": "text",
            "style": "width: 200px;",
            "placeholder": "example day & time",
        },
    )


class CrontabDailyForm(forms.Form):
    hour = forms.IntegerField()
    hour.widget.attrs.update(
        {
            "class": "form-control",
            "min": 0,
            "max": 23,
            "type": "number",
            "style": "width: 100px;",
            "placeholder": "0 - 23",
        },
    )
    minute = forms.IntegerField()
    minute.widget.attrs.update(
        {
            "class": "form-control",
            "min": 0,
            "max": 59,
            "type": "number",
            "style": "width: 100px;",
            "placeholder": "0 - 59",
        },
    )
    task_name = forms.CharField(max_length=50)
    task_name.widget.attrs.update(
        {
            "class": "form-control",
            "type": "text",
            "style": "width: 200px;",
            "placeholder": "example time task",
        },
    )
