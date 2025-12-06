# blog/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .forms import CustomUserCreationForm, UserUpdateForm, PostForm, CommentForm
from .models import Profile, Post, Comment

# ---------------------------
# AUTHENTICATION VIEWS
# ---------------------------


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("profile")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "blog/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, "blog/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
        else:
            messages.error(request, "Please fix the errors.")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "blog/profile.html", {"form": form})


# ---------------------------
# TAG HANDLING MIXIN
# ---------------------------


class TagHandlingMixin:
    """
    Mixin to parse the `tags` field from PostForm (comma-separated string)
    and sync it with the Post.tags many-to-many field.
    """

    def _save_tags(self, form):
        tags_str = form.cleaned_data.get("tags", "") or ""
        tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]

        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        # self.object is the saved Post instance
        self.object.tags.set(tags)


# ---------------------------
# BLOG POSTS CRUD
# ---------------------------


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"  # REQUIRED by tests
    context_object_name = "posts"
    ordering = ["-created_at"]


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # empty form for the "Add comment" section
        context["comment_form"] = CommentForm()
        return context


class PostCreateView(TagHandlingMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        self._save_tags(form)
        messages.success(self.request, "Post created.")
        return response

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})


class PostUpdateView(TagHandlingMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_initial(self):
        initial = super().get_initial()
        # pre-fill tags as comma-separated string
        initial["tags"] = ", ".join(
            self.object.tags.values_list("name", flat=True)
        )
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        self._save_tags(form)
        messages.success(self.request, "Updated")
        return response

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    login_url = "login"
    success_url = reverse_lazy("posts")

    def test_func(self):
        return self.get_object().author == self.request.user


# ---------------------------
# COMMENTS CRUD
# ---------------------------


@login_required
def comment_create(request, pk):
    """Create a comment on a given post, then redirect back to the post."""
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
        else:
            messages.error(request, "Please fix the errors in your comment.")

    return redirect("post-detail", pk=post.pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

    def get_context_data(self, **kwargs):
        # so that your template can use {{ comment }} like you wrote
        context = super().get_context_data(**kwargs)
        context["comment"] = self.object
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})


# ---------------------------
# TAG FILTER VIEW
# ---------------------------


def posts_by_tag(request, tag_name):
    """Show all posts that have a given tag."""
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all()
    return render(
        request,
        "blog/post_list.html",
        {"posts": posts, "active_tag": tag},
    )


# ---------------------------
# SEARCH VIEW
# ---------------------------


def post_search(request):
    """
    Search posts by title, content, or tag name.
    Query param: ?q=...
    """
    query = request.GET.get("q", "").strip()
    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()

    return render(
        request,
        "blog/search_results.html",
        {"query": query, "posts": posts},
    )
