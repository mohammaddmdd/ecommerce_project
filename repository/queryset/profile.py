from django.db.models import QuerySet


class ProfileQuerySet(QuerySet):
    
    def get_username(self):
        return self.username
