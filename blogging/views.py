from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.template import loader
from django.views.generic import ListView, DetailView
from django.views import View
from blogging.models import Post

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


#  rewrite our view
# def list_view(request):
# published = Post.objects.exclude(published_date__exact=None)
# posts = published.order_by('-published_date')
# context = {'posts': posts}
# return render(request, 'blogging/list.html', context)


class BlogListView(View):
    template_name = "blogging/list.html"

    def get(self, request):
        posts = (
            Post.objects.exclude(published_date__isnull=True)
            .filter(published_date__lte=timezone.now())
            .order_by("-published_date")
        )

        context = {"posts": posts}
        return render(request, self.template_name, context)


# def detail_view(request, post_id):
#   now = timezone.now()
# published = Post.objects.exclude(published_date__exact=None).filter(published_date__lte=now)
# print("Current time:", now)
# print("Trying to fetch post ID:", post_id)
# try:
# post = published.get(pk=post_id)
# return render(request, 'blogging/detail.html', {'post': post})
# except Post.DoesNotExist:
#   print(f"Post with ID {post_id} not found or not published.")
#  raise Http404("Post not found")


class BlogDetailView(DetailView):
    model = Post
    template_name = "blogging/detail.html"

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("pk")
        now = timezone.now()

        try:
            post = Post.objects.exclude(published_date__isnull=True).get(
                pk=post_id, published_date__lte=now
            )
        except Post.DoesNotExist:
            raise Http404("Post not found, check if unpublished")

        context = {"post": post}
        return render(request, self.template_name, context)
