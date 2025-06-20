from django.contrib import admin, messages
from .models import Build, Tag, BuildTag, Image
from django.utils.translation import ngettext

class BuildTagInline(admin.TabularInline):
    model = BuildTag
    extra = 0

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

# Register your models here.
@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'accepted']
    list_filter = ['creator', 'tags', 'accepted']
    search_fields = ['title', 'creator', 'tags']
    actions = ['markAccepted', 'markUnaccepted']
    inlines = [BuildTagInline, ImageInline]

    @admin.action(description="Accept Build(s)")
    def markAccepted(self, request, queryset):
        amountUpdated = queryset.update(accepted=True)

        self.message_user(
            request,
            ngettext(
                '%d build accepted successfully.',
                '%d builds accepted successfully.',
                amountUpdated
            )
            % amountUpdated,
            messages.SUCCESS
        )
    
    @admin.action(description="Unaccept Build(s)")
    def markUnaccepted(self, request, queryset):
        amountUpdated = queryset.update(accepted=False)

        self.message_user(
            request,
            ngettext(
                '%d build unaccepted successfully.',
                '%d builds unaccepted successfully.',
                amountUpdated
            )
            % amountUpdated,
            messages.SUCCESS
        )



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'accepted']
    list_filter = ['accepted']
    search_fields = ['name']
    actions = ['markAccepted', 'markUnaccepted']
    inlines = [BuildTagInline]

    @admin.action(description="Accept Tag(s)")
    def markAccepted(self, request, queryset):
        amountUpdated = queryset.update(accepted=True)

        self.message_user(
            request,
            ngettext(
                '%d tag accepted successfully.',
                '%d tags accepted successfully.',
                amountUpdated
            )
            % amountUpdated,
            messages.SUCCESS
        )
    
    @admin.action(description="Unaccept Tag(s)")
    def markUnaccepted(self, request, queryset):
        amountUpdated = queryset.update(accepted=False)

        self.message_user(
            request,
            ngettext(
                '%d tag unaccepted successfully.',
                '%d tags unaccepted successfully.',
                amountUpdated
            )
            % amountUpdated,
            messages.SUCCESS
        )

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'build', 'thumbnail']
    list_filter = ['build', 'thumbnail']
    search_fields = ['name', 'build']
