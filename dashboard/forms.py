from ckeditor.widgets import CKEditorWidget
from django import forms
class DescForm(forms.Form):
    description = forms.CharField(widget = CKEditorWidget())