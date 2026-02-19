from django.contrib import admin

from .models import Paper


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "author", "created_at", "updated_at")
	list_filter = ("author", "created_at", "updated_at")
	search_fields = ("title", "content", "author")
	ordering = ("-created_at",)
