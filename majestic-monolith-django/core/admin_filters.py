from django.contrib import admin


class UserIsActiveFilter(admin.SimpleListFilter):
    title = "Active"
    parameter_name = "Active"

    def lookups(self, request, model_admin):
        return (
            (False, "NO"),
            ("ALL", "ALL"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset.filter(is_active=True)
        if value == "ALL":
            return queryset
        return queryset.filter(is_active=value)

    def choices(self, changelist):
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string(remove=[self.parameter_name]),
            "display": "YES",
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }
