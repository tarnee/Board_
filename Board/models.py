from django.db import models


# Create your models here.
class Section(models.Model):
    # a, vg, b, etc
    name_section = models.CharField(max_length=3)

    # tv, video games, music, etc
    description = models.CharField(max_length=25)

    def __str__(self):
        return "%s %s" % (self.name_section, self.description)


class Thread(models.Model):
    # League of legends, World of Tanks, Toradora
    name_thread = models.CharField(max_length=30)

    # anonymous
    name_author = models.CharField(max_length=30, default="Anonymous")

    # 31 august 2016
    date_pub = models.DateTimeField()

    last_date_pub = models.DateTimeField()

    # number of original post in the section
    original_post_number = models.IntegerField(default=1)

    # number of posts in this thread
    thread_posts_number = models.IntegerField(default=0)

    # Hello, my name is Karen, I'm from Mexico
    original_post = models.CharField(max_length=1000)

    # the foreign key
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_thread


class Post(models.Model):
    # anonymous 2
    name_author = models.CharField(max_length=30, default="Anonymous")

    # 1 september 2016
    date_pub = models.DateTimeField()

    # number of post in the section
    post_number = models.IntegerField(default=1)

    # Hello, Karen, how are you?
    message = models.CharField(max_length=1000)

    # the foreign key
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def __str__(self):
        return self.message + " - " + self.thread.name_thread


class PostCounter(models.Model):
    post_number = models.IntegerField(default=0)
    threads_number = models.IntegerField(default=0)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        strings = self.section.name_section
        return strings + " " + str(self.post_number) + " постов, " + str(self.threads_number) + " тредов"

