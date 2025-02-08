import fitz
from django.db import models
from Account.models import AccountModel
class FileModel(models.Model):
    account = models.ForeignKey(AccountModel, on_delete=models.PROTECT, null=True)
    file = models.FileField(upload_to="files/", null=True)
    num_pages = models.IntegerField(null=True, blank=True)
    file_format = models.CharField(verbose_name="Format", max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trash = models.BooleanField(null=True, default=False)
    request_type = models.CharField(max_length=20, null=True)
    def __str__(self):
        return f"{self.file}.{self.file_format}"

    def save(self, *args, **kwargs):
        if self.file and not self.num_pages:
            self.file_format = self._get_file_format()
            self.num_pages = self._get_file_page_count()
        super().save(*args, **kwargs)

    def _get_file_format(self):
        return self.file.name.split(".")[-1]


    def _get_file_page_count(self):
        if self.file_format.lower() == 'pdf':
            with fitz.open(stream=self.file.read(), filetype="pdf") as pdf:
                return pdf.page_count
        elif self.file_format.lower() == 'html':
            return 1
        else:
            return None

    def get_file_path(self):
        return self.file

    def get_account(self):
        return self.account

    def get_num_pages(self):
        return self.num_pages
