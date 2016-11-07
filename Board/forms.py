from django.forms import ModelForm, Textarea, HiddenInput
from .models import Thread, Post, ImagesOfPost
from captcha.fields import CaptchaField


class NewThreadForm(ModelForm):

    captcha = CaptchaField()

    class Meta:
        model = Thread

        fields = ('name_thread', 'name_author', 'original_post')
        widgets = {
            'original_post': Textarea(attrs={'cols': 70, 'rows': 7}),


        }
        labels = {
            
            'original_post': "Текст",
            'name_author': "Имя",
            'name_thread': "Тема",

        }


class NewPostForm(ModelForm):

    captcha = CaptchaField()

    class Meta:
        model = Post
        fields = ('name_author', 'message', 'thread')
        widgets = {
            'message': Textarea(attrs={'cols': 70, 'rows': 3}),
            'thread': HiddenInput()
        }
        labels = {
            'name_author': "Имя",
            'message': "Текст",
        }


class NewImageForm(ModelForm):
    class Meta:
        model = ImagesOfPost
        fields = ('image',
                  )
        labels = {'image': 'Картинка',
                  }

