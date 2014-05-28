from rango.models import Page, Category
from django import forms
from django.contrib.auth.models import User
from rango.models import UserProfile

#this file stores form related classes
#ModelForm class
class CategoryForm(forms.ModelForm):
	name=forms.CharField(max_length=128,help_text="please enter the category name")
	views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)#the input is hidden
	likes=forms.IntegerField(widget=forms.HiddenInput(),initial=0)
	#an inline class to provide additional information on the formm
	class Meta:
		model=Category#all the fields are included

class PageForm(forms.ModelForm):
	title=forms.CharField(max_length=128,help_text="please enter the page title")
	url=forms.URLField(max_length=200,help_text="please enter the page url")
	views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)
	def clean(self):
		cleaned_data=self.cleaned_data
		url=cleaned_data['url']
		if url and not url.startswith('http://'):
			url='http://'+url
			cleaned_data['url']=url
		return cleaned_data
	class Meta:
		model=Page
		fields=('title','url','views')
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website',)#the one to one abstraction with the User model is alright
