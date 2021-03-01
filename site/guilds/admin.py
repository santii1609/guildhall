from django.contrib import admin

# Register your models here.
from .models import Guild, Description



#admin.site.register(Description)


class DescriptionInline(admin.TabularInline):

    model = Description
    extra = 3

class GuildAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': ['creation_date']}),
    ]
    inlines = [DescriptionInline]

admin.site.register(Guild, GuildAdmin)
