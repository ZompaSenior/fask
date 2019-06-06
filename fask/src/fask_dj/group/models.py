from django.db import models
from base.models import FaskObject, EditInfo, StandardForm

class Group(FaskObject, EditInfo):
    pass
# Create your models here.
class GroupForm(StandardForm):
    class Meta:
        model = Group
        fields = '__all__'