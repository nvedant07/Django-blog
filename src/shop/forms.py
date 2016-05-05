from django import forms


class signinform(forms.Form):
	email=forms.EmailField()
	password=forms.CharField(widget=forms.PasswordInput)

class signupform(forms.Form):
	firstname=forms.CharField()
	lastname=forms.CharField()
	email=forms.EmailField()
	password=forms.CharField(widget=forms.PasswordInput)
	re_type_password=forms.CharField(widget=forms.PasswordInput)
	
	
	def clean_passwords(self):
		pass1=self.cleaned_data.get("password")
		pass2=self.cleaned_data.get("re_type_password")
		if(pass1 and pass2 and pass1!=pass2):
			raise forms.ValidationError("Password do not match")
		return pass2
class passform(forms.Form):
	email=forms.EmailField()
class changepassform(forms.Form):
	# email=forms.EmailField()
	current_password=forms.CharField(widget=forms.PasswordInput)
	new_password=forms.CharField(widget=forms.PasswordInput)
	re_type_new_password=forms.CharField(widget=forms.PasswordInput)

class newblog(forms.Form):
	title=forms.CharField()
	content=forms.CharField(widget=forms.Textarea,required=False)
