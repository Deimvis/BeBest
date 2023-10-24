from django.contrib import admin

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'published', 'canonized_url', 'rank', 'source_name')

    @admin.display(ordering="publish_timestamp")
    def published(self, obj: Post):
        from datetime import datetime
        return datetime.fromtimestamp(obj.publish_timestamp)
