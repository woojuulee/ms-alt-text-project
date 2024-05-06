from django.db import models
from django.core.files.storage import default_storage

# Create your models here.
class UploadedFile(models.Model):
    id = models.AutoField(primary_key=True)
    file_path = models.ImageField(upload_to='')  # 업로드된 파일을 저장할 경로 설정

    def __str__(self):
        return self.file_path.name

class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, null=True)
    name = models.CharField(default="", max_length=255)
    alt_text = models.TextField(null=False, default="")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        print('alt_text :', self.alt_text)
        return self.name
    
