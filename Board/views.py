from django.shortcuts import render, get_object_or_404
from .models import Section, Thread, Post, PostCounter
from .forms import NewThreadForm, NewPostForm
from django.utils import timezone


# Create your views here
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
            this_thread.save()

            post_count.save()
            new_post.save()

    post_arrange = []

    thread_list = Thread.objects.filter(section__name_section__exact=section_id).order_by('-last_date_pub')

    post_c = get_object_or_404(PostCounter, section=section.id)
    for i in range(0, post_c.threads_number):
        post_arrange.append(Post.objects.filter(thread__exact=thread_list[i]))

    zip_list = list(zip(thread_list, post_arrange))

    context = {'section_list': section_list,
               'this_section': Section.objects.filter(name_section__exact=section_id)[0],
               'thread_list': thread_list,
               'post_list': thread_list,
               'zip_list': zip_list,
               'thread_form': NewThreadForm(),
               'post_form': NewPostForm(),
               }
    return render(request, 'Board/section.html', context)


def index(request):
    section_list = Section.objects.all
    context = {'section_list': section_list,
               }
    return render(request, 'Board/index.html', context)
