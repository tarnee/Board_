from django.shortcuts import render, get_object_or_404
from .models import Section, Thread, Post, PostCounter, ImagesOfOriginalPost, ImagesOfPost
from .forms import NewThreadForm, NewPostForm, NewImageForm
from django.utils import timezone


def section(request, section_id):

    section_list = Section.objects.all
    section = get_object_or_404(Section, name_section=section_id)
    if request.method == "POST" and 'new_thread' in request.POST:
        form = NewThreadForm(request.POST)

        if form.is_valid():
            new_thread = form.save(commit=False)

            new_thread.date_pub = timezone.now()
            new_thread.last_date_pub = new_thread.date_pub

            post_count = get_object_or_404(PostCounter, section=section.id)
            post_count.threads_number += 1
            post_count.post_number += 1
            new_thread.original_post_number = post_count.post_number

            new_thread.thread_number = post_count.threads_number
            new_thread.section = section

            post_count.save()
            new_thread.save()

    elif request.method == "POST" and 'new_post' in request.POST:
        form = NewPostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            post_count = get_object_or_404(PostCounter, section=section.id)

            post_count.post_number += 1

            new_post.date_pub = timezone.now()
            new_post.post_number = post_count.post_number

            this_thread = new_post.thread
            this_thread.last_date_pub = new_post.date_pub
            this_thread.thread_posts_number += 1
            this_thread.save()
            post_count.save()
            new_post.save()

            image_form = NewImageForm(request.POST, request.FILES)
            if image_form.is_valid() and request.FILES:
                for img in request.FILES.getlist('image'):
                    ImagesOfPost.objects.create(name=img.name, post=new_post, image=img)

    thread_list = section.threads.all()[0:9]

    original_post_image = [ImagesOfOriginalPost.objects.get(thread__exact=x) for x in thread_list]

    post_list = [x.posts_in_thread.all() if x.thread_posts_number <= 5 else x.posts_in_thread.all(

    )[x.thread_posts_number-5:]
                 for x in thread_list]

    image_list = [[some_post.img.all() for some_post in thread_l]
                  for thread_l in post_list]

    zip_list = zip(thread_list, original_post_image, post_list, image_list)

    file_form_list = [NewImageForm() for i in range(4)]

    context = {'section_list': section_list,
               'this_section': section,
               'thread_list': thread_list,
               'post_list': thread_list,
               'zip_list': zip_list,
               'thread_form': NewThreadForm(),
               'post_form': NewPostForm(),
               'image_form': file_form_list,
               }
    return render(request, 'Board/section.html', context)


def index(request):
    section_list = Section.objects.all
    context = {'section_list': section_list,
               }
    return render(request, 'Board/index.html', context)

