from django.db.models import Manager

from django.db.models.query import QuerySet


class CommonBaseManager(Manager):
    def all_actives(
        self,
    ):
        queryset = self.filter(
            is_deleted=False,
        )

        return queryset

    def permanently_delete_marked(
        self,
    ):
        queryset = self.filter(
            is_deleted=True,
        )
        count = queryset.count()
        try:
            queryset.delete()
            return True, count
        except Exception as error:
            return False, error

    def bulk_mark_delete(self, queryset: QuerySet):
        if queryset is None:
            return True, 0

        count = queryset.count()
        try:
            for instance in queryset:
                instance.safe_delete(commit=False)
            queryset.bulk_update(queryset, ["is_deleted"])
            return True, count
        except Exception as error:
            return False, error

    def safe_create(self, **fields):
        """
        To making sure Django-Storage would not override our create method,
            and broke the save process,
            Please using .safe_create() for file base models.
        """
        instance = self.model(**fields)
        instance.save(using=self._db)
        return instance

    def get_queryset(self):
        qs = super().get_queryset()

        # Get the project if this model has a direct reference
        if hasattr(self.model, "project"):
            return qs.select_related("project")

        # For models that might have indirect project references
        if any(f.name == "site" for f in self.model._meta.fields):
            return qs.select_related("site__project")

        return qs
