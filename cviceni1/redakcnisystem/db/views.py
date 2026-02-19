from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from .models import Paper


class IndexView(TemplateView):
	template_name = "db/index.html"


class ArticleListView(ListView):
	model = Paper
	template_name = "db/article_list.html"
	context_object_name = "articles"
	queryset = Paper.objects.all().order_by("-created_at")


class ArticleDetailView(DetailView):
	model = Paper
	template_name = "db/article_detail.html"
	context_object_name = "article"


class ArticleCreateView(View):
	def get(self, request):
		return render(request, "db/article_form.html", {"action": "Vytvořit"})

	def post(self, request):
		title = request.POST.get("title", "").strip()
		content = request.POST.get("content", "").strip()
		author = request.POST.get("author", "").strip()

		if title and content and author:
			article = Paper.objects.create(title=title, content=content, author=author)
			return redirect("db:article_detail", pk=article.pk)

		return render(
			request,
			"db/article_form.html",
			{
				"action": "Vytvořit",
				"error": "Vyplňte title, content a author.",
				"article": {
					"title": title,
					"content": content,
					"author": author,
				},
			},
			status=400,
		)


class ArticleEditView(View):
	def get(self, request, pk):
		article = get_object_or_404(Paper, pk=pk)
		return render(request, "db/article_form.html", {"action": "Uložit", "article": article})

	def post(self, request, pk):
		article = get_object_or_404(Paper, pk=pk)

		title = request.POST.get("title", "").strip()
		content = request.POST.get("content", "").strip()
		author = request.POST.get("author", "").strip()

		if title and content and author:
			article.title = title
			article.content = content
			article.author = author
			article.save()
			return redirect("db:article_detail", pk=article.pk)

		return render(
			request,
			"db/article_form.html",
			{
				"action": "Uložit",
				"error": "Vyplňte title, content a author.",
				"article": {
					"title": title,
					"content": content,
					"author": author,
				},
			},
			status=400,
		)


class ArticleDeleteView(View):
	def get(self, request, pk):
		article = get_object_or_404(Paper, pk=pk)
		return render(request, "db/article_confirm_delete.html", {"article": article})

	def post(self, request, pk):
		article = get_object_or_404(Paper, pk=pk)
		article.delete()
		return redirect("db:article_list")
