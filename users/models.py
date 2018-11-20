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
            passport = self.get(username=username, password=get_hash(password))
            print('passport',passport)
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


class AddressManager(models.Manager):
    def get_default_address(self, passport_id):
        try:
            addr = self.get(passport_id=passport_id, is_default=True)
        except self.model.DoesNotExist:
            addr = None
        return addr

    def add_one_address(self, passport_id, recipient_name, recipient_addr, zip_code, recipient_phone):
        addr = self.get_default_address(passport_id=passport_id)
        # if there is not default address then new address to be default address
        if addr:
            is_default = False
        else:
            is_default = True

        addr = self.create(passport_id=passport_id,
                           recipient_name=recipient_name,
                           recipient_addr=recipient_addr,
                           zip_code=zip_code,
                           recipient_phone=recipient_phone,
                           is_default=is_default)
        return addr


class Address(BaseModel):
    recipient_name = models.CharField(max_length=20, verbose_name='signer_name')
    recipient_addr = models.CharField(max_length=256, verbose_name='signer_address')
    zip_code = models.CharField(max_length=6, verbose_name='postalcode')
    recipient_phone = models.CharField(max_length=11, verbose_name='signer_phone')
    is_default = models.BooleanField(default=False, verbose_name='the default address')
    passport = models.ForeignKey('Passport', on_delete=models.CASCADE, verbose_name='user account')


    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'

