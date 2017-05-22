from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.utils import timezone

from .settings import BOARD_THEME
from apps.api.models import (
    EmailUser, Category, Subcategory, Thread, Post, Report, Conversation,
    Message
)
from .forms import ThreadForm, PostForm, ReportForm


def base_context(request):
    ctx = {}
    if request.user.is_authenticated and not request.user.is_banned:
        unread_conversations = Conversation.objects.filter(
            unread_by__in=[request.user]).count()
        ctx.update({'unread_conversations': unread_conversations})
        if request.user.is_staff:
            unresolved_reports = Report.objects.filter(resolved=False).count()
            ctx.update({'unresolved_reports': unresolved_reports})
    return ctx


def index_view(request):
    category_groups = []
    parent_categories = Category.objects.all()
    if not request.user.is_authenticated:
        # Filter out categories with auth_req = True
        parent_categories = parent_categories.filter(
            auth_req=False).order_by('order')
    for parent_category in parent_categories:
        children = parent_category.subcategories
        if not request.user.is_authenticated:
            # Filter out categories with auth_req = True
            children = children.filter(auth_req=False).order_by('order')
        category_groups.append({
            'parent': parent_category,
            'children': children
        })
    recent_threads = Thread.objects.all().order_by('-created')
    recent_activity = Thread.objects.all().order_by('-modified')
    if not request.user.is_authenticated:
        # Filter out threads in subcategories with auth_req = True
        recent_threads = recent_threads.filter(
            category__auth_req=False)
        recent_activity = recent_activity.filter(
            category__auth_req=False)
    newest_member = EmailUser.objects.all().order_by('-created').first()
    member_count = EmailUser.objects.all().count()
    context = {
        'categories': category_groups,
        'recent_threads': recent_threads[:5],
        'recent_activity': recent_activity[:5],
        'newest_member': newest_member,
        'member_count': member_count
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/index.html'.format(BOARD_THEME), context)


def unpermitted_view(request):
    return render(request, 'board/themes/{}/unpermitted.html'.format(BOARD_THEME), {})


def my_profile(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')
    context = {}
    context.update(base_context(request))
    return render(request, 'board/themes/{}/my_profile.html'.format(BOARD_THEME), context)


def settings_view(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')
    context = {}
    context.update(base_context(request))
    return render(request, 'board/themes/{}/settings.html'.format(BOARD_THEME), context)


def profile_view(request, username):
    user = EmailUser.objects.get(username=username)
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')
    # Redirect to /board/me/ if trying to view own profile.
    if request.user.id == user.id:
        # TODO do not redirect so that users
        # can view their profile as others see it.
        return redirect('board:me')
    context = {
        'profile': user
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/profile_page.html'.format(BOARD_THEME), context)


def category_view(request, pk):
    category = Category.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have view
    # permissions on this category.
    if not category.can_view(request.user):
        return unpermitted_view(request)
    subcategories = []
    for sub in category.subcategories:
        subcategories.append({
            'obj': sub,
            'can_post': sub.can_post(request.user),
        })
    context = {
        'category': category,
        'subcategories': subcategories
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/category_view.html'.format(BOARD_THEME), context)


def subcategory_view(request, pk):
    category = Subcategory.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have view
    # permissions on this subcategory.
    if not category.can_view(request.user):
        return unpermitted_view(request)
    # Paginate threads
    paginator = Paginator(category.threads.order_by('-pinned', '-modified'), 20)
    page = request.GET.get('page')
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.page(paginator.num_pages)
    context = {
        'can_post': category.can_post(request.user),
        'category': category,
        'threads': threads
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/subcategory_view.html'.format(BOARD_THEME), context)


def thread_view(request, pk):
    thread = Thread.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have view
    # permissions on this thread.
    if not thread.can_view(request.user):
        return unpermitted_view(request)
    # Paginate posts
    paginator = Paginator(thread.posts.order_by('created'), 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # Logic for creating a new post on a thread
    if request.method == 'POST':
        # Redirect to unpermitted page if not logged in.
        if not request.user.is_authenticated:
            return unpermitted_view(request)
        form = PostForm(request, request.POST)
        if form.is_valid():
            form.save(thread=thread, set_user=True)
            # Redirect to the last page of posts,
            # which is where this new post will be.
            return redirect('/board/thread/{}/?page={}'.format(
                thread.id, paginator.num_pages))
    else:
        form = PostForm(request)
    context = {
        'thread': thread,
        'posts': posts,
        'post_form': form,
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/thread_view.html'.format(BOARD_THEME), context)


def thread_create(request, category_id):
    subcategory = Subcategory.objects.get(id=category_id)
    # Redirect to unpermitted page if the requesting user does not have post
    # permission in this category.
    if not subcategory.can_post(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        form = ThreadForm(request, request.POST)
        if form.is_valid():
            thread = form.save(category=subcategory, set_user=True)
            return redirect('board:thread', thread.id)
    else:
        form = ThreadForm(request)
    context = {
        'form': form
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/thread_create_form.html'.format(BOARD_THEME), context)


def thread_update(request, pk):
    instance = Thread.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this thread.
    if not instance.can_edit(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        form = ThreadForm(request, request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('board:thread', pk)
    else:
        form = ThreadForm(request, instance=instance)
    context = {
        'form': form
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/thread_update_form.html'.format(BOARD_THEME), context)


def thread_delete(request, pk):
    instance = Thread.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this thread.
    if not instance.can_edit(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        redirect_to = instance.category.id
        instance.delete()
        return redirect('board:subcategory', redirect_to)
    context = {
        'object': instance
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/thread_delete_form.html'.format(BOARD_THEME), context)


# There is no post_view or post_create as both are handled on the thread_view

def post_update(request, pk):
    instance = Post.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this post.
    if not instance.can_edit(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        form = PostForm(request, request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('board:thread', instance.thread.id)
    else:
        form = PostForm(request, instance=instance)
    context = {
        'form': form
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/post_update_form.html'.format(BOARD_THEME), context)


def post_delete(request, pk):
    instance = Post.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this post.
    if not instance.can_edit(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        redirect_to = instance.thread.id
        instance.delete()
        return redirect('board:thread', redirect_to)
    context = {
        'object': instance
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/post_delete_form.html'.format(BOARD_THEME), context)


def conversations_list(request):
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this post.
    if request.user.is_authenticated and request.user.is_banned:
        return redirect('board:unpermitted')
    conversations = request.user.conversations.all()
    context = {
        'conversations': conversations
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/conversations_list.html'.format(BOARD_THEME), context)


def reports_list(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned or is not an admin
    if not request.user.is_authenticated or \
        not request.user.is_staff or request.user.is_banned:
        return redirect('board:unpermitted')
    context = {
        'reports': Report.objects.all()
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/reports_list.html'.format(BOARD_THEME), context)


def report_view(request, pk):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned or is not an admin
    if not request.user.is_authenticated or \
        not request.user.is_staff or request.user.is_banned:
        return redirect('board:unpermitted')
    instance = Report.objects.get(id=pk)
    if request.method == 'POST':
        instance.resolved = True
        instance.resolved_by = request.user
        instance.date_resolved = timezone.now()
        instance.save()
        return redirect('board:reports-list')
    context = {
        'report': Report.objects.get(id=pk)
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/report_view.html'.format(BOARD_THEME), context)


def report_create(request, thread=None, post=None):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')
    if request.method == 'POST':
        form = ReportForm(request, request.POST)
        if form.is_valid():
            if thread:
                thread_obj = Thread.objects.get(id=thread)
                report = form.save(thread=thread_obj, set_user=True)
                return redirect('board:thread', thread)
            if post:
                post_obj = Post.objects.get(id=post)
                report = form.save(post=post_obj, set_user=True)
                return redirect('board:thread', post_obj.thread.id)
    else:
        form = ReportForm(request)
    context = {
        'form': form
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/report_create_form.html'.format(BOARD_THEME), context)


def members_list(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')
    users = EmailUser.objects.order_by('username')
    context = {
        'users': users
    }
    context.update(base_context(request))
    return render(request, 'board/themes/{}/members_list.html'.format(BOARD_THEME), context)
