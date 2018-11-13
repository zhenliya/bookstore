from db.base_model import BaseModel
from utils.get_hash import get_hash
from django.db import models
# Create your models here.

class PassportManager(models.Manager):
    def add_one_passport(self, username, password, email):
        passport = self.create(username=username, password=get_hash(password), email=email)
        return passport

    def get_one_passport(self, username, password):
        try:
            passport = serlf.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
            passport = None
        return passport
    

class Passport(BaseModel):
    username = models.CharField(max_length=20, unique=True, verbose_name='username')
    password = models.CharField(max_length=40, verbose_name='password')
    email = models.EmailField(verbose_name='email')
    is_active = models.BooleanField(default= False, verbose_name='active status')

    objects = PassportManager()


    class Meta:
        db_table = 's_user_account'
