# Third-party imports
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F, Q
from django.contrib import messages

# Local application imports
from .models import Comment, Category, Post, CommentReply


# Create your views here.

class ModelMixin:
    def get_queryset(self):
        return super().get_queryset().all()


class PostFormMixin(ModelMixin):
    fields = ['title', 'details', 'picture', 'category']
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message


class FormSuperUserMessageMixin:
    success_message = ''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message


def index(request):
    post = Post.objects.all()
    featured_post = Post.objects.filter(is_featured=True)[:3]
    popular_post = Post.objects.all().order_by('-no_of_views')[:3]
    recent_post = Post.objects.all().order_by('-created')[:3]
    category = Category.objects.all()

    context = {
        'post': post,
        'featured_post': featured_post,
        'recent_post': recent_post,
        'category': category,
        'popular_post': popular_post,
    }
    return render(request, 'blogapp/index.html', context)


def post_detail(request, category_id, post_id):
    all_categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    post = get_object_or_404(Post, pk=post_id, category_id=category_id)
    post.no_of_views = F('no_of_views') + 1
    post.save()
    post_comment = post.comment_set.all()
    post.refresh_from_db(fields=['no_of_views'])
    if request.method == 'POST':
        if 'comment_form' in request.POST:
            if request.user.is_authenticated:
                owner = request.user
            else:
                owner = None
            # post = post
            details = request.POST.get('comment')
            comment = Comment.objects.create(owner=owner, post=post, details=details)
            comment.save()
        elif 'reply_form' in request.POST:
            if request.user.is_authenticated:
                owner = request.user
            else:
                owner = None
            comment_id = request.POST.get('comment_id')
            details = request.POST.get('reply')
            comment = Comment.objects.get(pk=comment_id)
            reply = CommentReply.objects.create(owner=owner, comment=comment, reply=details)
            reply.save()

    context = {
        'post': post,
        'category': category,
        'all_categories': all_categories,
        'post_comment': post_comment,
    }
    return render(request, 'blogapp/single-page.html', context)


class CreatePost(PostFormMixin, ModelMixin, CreateView):
    model = Post
    template_name = 'blogapp/create_post.html'
    success_message = 'post created successfully'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class UpdatePost(PostFormMixin, ModelMixin, UpdateView):
    model = Post
    template_name = 'blogapp/update_post.html'
    success_message = 'post updated successfully'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class DeletePost(PostFormMixin, ModelMixin, DeleteView):
    model = Post
    template_name = 'blogapp/confirm_delete.html'
    success_url = '/'
    success_message = 'post deleted successfully'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class DeleteComment(ModelMixin, FormSuperUserMessageMixin, DeleteView):
    model = Comment
    template_name = 'blogapp/confirm_delete.html'
    success_url = '/'
    success_message = 'comment deleted successfully'


def CreateUserAccount(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'account creation successful')
                return redirect('index')
            else:
                print("Authentication failed")
    else:
        form = UserCreationForm()
    return render(request, 'blogapp/create_account.html', context={'form': form})


class SearchResultsView(ModelMixin, ListView):
    model = Post
    template_name = "blogapp/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return super().get_queryset().filter(
            Q(title__icontains=query)
        )


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print(name, email, message, subject)
    context = {

    }
    return render(request, 'blogapp/contact.html')
