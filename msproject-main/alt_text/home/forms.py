from django import forms
from django.forms import ModelForm
from .models import Goods, UploadedFile

class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        # fields = '__all__'
        fields = ['file_path']

        widgets = {
            'file_path': forms.FileInput(attrs={'class': 'form-control'}),
        }

class GoodsForm(ModelForm):
    class Meta:
        model = Goods
        fields = ['name', 'alt_text', 'image'] # "__all__" ('name', 'OCR', ...)
        labels = {
            'name':'상품명',
            'alt_text':'상품정보',
        }

        widgets = {
            'name':forms.Textarea(attrs={'class':'form-control', 'placeholder': '상품명을 입력해주세요.'}),
            'alt_text':forms.Textarea(attrs={'class':'form-control'}),
        }


