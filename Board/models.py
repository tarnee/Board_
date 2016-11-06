from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.


class Section(models.Model):
    # a, vg, b, etc
    name_section = models.CharField(max_length=3)

    # tv, video games, music, etc
    description = models.CharField(max_length=25)

    def __str__(self):
        return "%s %s" % (self.name_section, self.description)


class Thread(models.Model):
    class Meta:
        ordering = ['-last_date_pub']
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
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="threads")

    def __str__(self):
        return self.section.name_section + " " + self.name_thread


class Post(models.Model):
    # anonymous 2
    name_author = models.CharField(max_length=30, default="Anonymous")

    # 1 september 2016
    date_pub = models.DateTimeField()

    number_of_image = models.IntegerField(default="0")

    # number of post in the section
    post_number = models.IntegerField(default=1)

    # Hello, Karen, how are you?
    message = models.CharField(max_length=1000)

    # the foreign key
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts_in_thread")

    def __str__(self):
        return self.message + " - " + self.thread.name_thread


class PostCounter(models.Model):
    post_number = models.IntegerField(default=0)
    threads_number = models.IntegerField(default=0)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="counter")

    def __str__(self):
        strings = self.section.name_section
        return strings + " " + str(self.post_number) + " постов, " + str(self.threads_number) + " тредов"


def user_directory_path(instance, filename):
    return "Media/{0}/{1}/{2}_{3}".format(instance.thread.section.name_section, instance.thread.id,
                                          str(instance.id), filename)


def get_name(instance, filename):
    x, y = filename
    return x


class ImagesOfOriginalPost(models.Model):
    name = models.CharField(max_length=50)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(300, 200)],
                                     format='JPEG',
                                     options={'quality': 80})

    def __str__(self):
        string = " ".join([self.thread.section.name_section, self.thread.name_thread, "1"])
        return string


def user_directory_path_post(instance, filename):
    return "Media/{0}/{1}/{2}_{3}".format(instance.post.thread.section.name_section,
                                          instance.post.thread.id, instance.id,
                                          filename)


class ImagesOfPost(models.Model):

    name = models.CharField(max_length=6, default="image1")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="img")
    image = models.ImageField(upload_to=user_directory_path_post, blank=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(300, 200)],
                                     format='JPEG',
                                     options={'quality': 80})

    def __str__(self):
        string = " ".join([self.post.thread.section.name_section, self.post.thread.name_thread,
                           str(self.post.post_number), self.name])
        return string


@receiver(pre_delete, sender=ImagesOfOriginalPost)
def delete_op_post(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)

