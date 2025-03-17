from django.db import models

from ..managers import CommonBaseManager


class CommonBaseModel(models.Model):
    """
    this is an abstract model
    We inherit this table for most of our tables to add latest created and updated in table
    is_deleted is a property when we don't want to actually delete something, and we just
        don't want to show it to the user
    """

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    # these field become nullable because we are interacting with another schemas
    # So we have to add these three in them too.

    objects = CommonBaseManager()

    class Meta:
        abstract = True

    def safe_delete(
        self,
        commit=False,
    ):
        # this method only set is_deleted attribute to True
        self.is_deleted = True
        if commit:
            self.save()
