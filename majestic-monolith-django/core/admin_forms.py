from django import forms


class AdminCacheQueryForm(forms.Form):
    key_prefix = forms.CharField(help_text="key_prefix of cache")
