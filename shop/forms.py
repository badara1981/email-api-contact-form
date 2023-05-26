# import the forms module
from django import forms
from django.core.exceptions import ValidationError 
from django.core import validators
from django.forms import CharField

from django.core.validators import validate_email

# inherit from forms.Form

# organization
CAR_CHOICES = (
    ("bmw", "BMW"),
    ("tesla", "Tesla"),
    ("fiat", "Fiat"),
    ("audi", "Audi"),
)


class CarSearch(forms.Form):
    start_date = forms.DateField(
        label="When do you want to take car?", widget=forms.SelectDateWidget
    )
    end_date = forms.DateField(
        label="when to bring back car?", widget=forms.SelectDateWidget
    )
    cars = forms.CharField(
        initial="fiat",
        label="Choose your car",
        widget=forms.Select(choices=CAR_CHOICES),
        help_text="All our cars are premium, if you scratch you pay!",
    )



class SearchForm(forms.Form):
    
 
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()

    cc_myself = forms.BooleanField(required=False)



    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        if "badara.jammeh@example.com" not in data:
            raise ValidationError("You have forgotten about Badara!")


class MultiEmailField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
           validate_email(email)




class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()  # some validations in frontend
    reason = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject:
            # Only do something if both fields are valid so far.
            if "help" not in subject:
                raise ValidationError(
                    "Did not send for 'help' in the subject despite "
                    "CC'ing yourself."
                )


        if cc_myself and subject and "help" not in subject:
            msg = "Must put 'help' in subject when cc'ing yourself."
            self.add_error('cc_myself', msg)
            self.add_error('subject', msg)


class HotelSearch(forms.Form):
    start_date = forms.DateField(label="Checkin", widget=forms.SelectDateWidget)
    end_date = forms.DateField(label="Checkout", widget=forms.SelectDateWidget)

""" 
def validate_email(value):
    if 'wtf' in value:
        raise ValidationError("Sorry, we want a nicer email")  """