from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Article, Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from.serializers import (
    ArticleSerializer,
    CommentSerializer,
    ArticleDetailSerializer,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

# @api_view(["GET", "POST"])
# def article_list(request):
#     if request.method == "GET":
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def article_detail(request, pk):
#     article = get_object_or_404(Article, pk=pk)
#     if request.method == "GET":
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         article = get_object_or_404(Article, pk=pk)
#         serializer = ArticleSerializer(article, data=request.data,partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)

#     elif request.method == "DELETE":
#         article.delete()
#         data = {"delete": f"Article({pk}) is deleted."}
#         return Response(data, status=status.HTTP_204_NO_CONTENT)

class ArticleListAPIView(APIView):

    permission_classes=[IsAuthenticated]
    @extend_schema(
        tags=["Articles"],
        description="Article 목록 조회를 위한 API",
    )
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    @extend_schema(
        tags=["Articles"],
        description="Article 생성을 위한 API",
        request=ArticleSerializer,
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):

    permission_classes=[IsAuthenticated]

		# 두 번 이상 반복되는 로직은 함수로 빼면 좋습니다👀
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        data = {"pk": f"{pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)

class CommentListAPIView(APIView):

    permission_classes=[IsAuthenticated]

    def get(self, request, pk):
        article=get_object_or_404(Article, pk=pk)
        comments=article.comments.all()
        serializers=CommentSerializer(comments, many=True)
        return Response(serializers.data)
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

from .models import Article , Comment

class CommentDetailAPIView(APIView):
    
    permission_classes=[IsAuthenticated]
    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        data = {"pk": f"{comment_pk} is deleted."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        


@api_view(["GET"])
def check_sql(request):
    from django.db import connection
    #역참조
    articles = Article.objects.all().prefetch_related("comments")
    for article in articles:
        comments=article.comments.all()
        for comment in comments:
            print(comment.content)
    print("-" * 30)
    print(connection.queries)

    return Response()

    #정참조
    # comments = Comment.objects.all().select_related("article")
    # for comment in comments:
    #     print(comment.article.title)  
    # print("-" * 30)
    # print(connection.queries)

    # return Response()

# def article_list_html(request):
#     articles = Article.objects.all()
#     context = {"articles": articles}
#     return render(request, "articles/articles.html", context)


# def json_01(request):
#     articles = Article.objects.all()
#     json_res = []

#     for article in articles:
#         json_res.append(
#             {
#                 "title": article.title,
#                 "content": article.content,
#                 "created_at": article.created_at,
#                 "updated_at": article.updated_at,
#             }
#         )
#     return JsonResponse(json_res, safe=False)


# def json_02(request):
#     articles = Article.objects.all()
#     res_data = serializers.serialize("json", articles)
#     return HttpResponse(res_data, content_type="application/json")

# @api_view(["GET"])
# def json_drf(request):
#     articles = Article.objects.all()
#     serializer = ArticleSerializer(articles, many=True)
#     return Response(serializer.data)
