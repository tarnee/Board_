from django.contrib import admin
from .models import Section, Thread, Post, PostCounter, ImagesOfOriginalPost, ImagesOfPost

admin.site.register(Section)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(PostCounter)
admin.site.register(ImagesOfOriginalPost)
admin.site.register(ImagesOfPost)
# Register your models here.
