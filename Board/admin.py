from django.contrib import admin

from .models import Section, Thread, Post, PostCounter

admin.site.register(Section)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(PostCounter)

# Register your models here.