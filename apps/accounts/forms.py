from django import forms
from apps.accounts.models import CustomAccount, Profile
from apps.utils.password_validations import (contains_digits, contains_lowercase, contains_uppercase,
                                             does_not_contains_symbols, does_not_contains_whitespace)


class AccountRegistrationForm(forms.ModelForm):
    """ A form for creating new users. Includes all the required
    fields, plus a repeated password. """

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                               required=True, validators=[contains_digits, contains_lowercase, contains_uppercase,
                                                          does_not_contains_symbols, does_not_contains_whitespace],
                               min_length=8)
    password_confirm = forms.CharField(label='Password confirmation',
                                       widget=forms.PasswordInput(
                                           attrs={'placeholder': 'Confirm Password'}),
                                       required=True,
                                       validators=[contains_digits, contains_lowercase, contains_uppercase,
                                                   does_not_contains_symbols, does_not_contains_whitespace],
                                       min_length=8)

    class Meta:
        model = CustomAccount
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean(self):
        taken_email = CustomAccount.objects.filter(email=self.cleaned_data['email']).exists()
        # Check that the two password entries match
        if self.is_valid():
            password = self.cleaned_data["password"]
            password_confirm = self.cleaned_data["password_confirm"]
            if password != password_confirm:
                self.add_error('password', "Passwords don't match")
            # Check That Email Exists Or Not
            if taken_email:
                self.add_error('email', 'This Email Is Already Taken')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AccountAuthenticationForm(forms.ModelForm):
    """ A form for existing users. Includes all the required
        fields for user to authenticate. """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
                               )

    class Meta:
        model = CustomAccount
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            credential = self.cleaned_data['email']
            existing_user = CustomAccount.objects.filter(email=credential).exists()
            if not existing_user:
                self.add_error('email', "Credentials Are Wrong")


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea, required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'profile_picture', 'gender', 'date_of_birth')
