from django.db.models import Manager

from account.repository.queryset import ProfileQuerySet


class ProfileDataAccessLayerManager(Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)
