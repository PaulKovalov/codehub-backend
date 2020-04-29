import json
import time

import redis
from django.conf import settings
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from articles.models import Article
from articles.serializers import ArticlePreviewSerializer
from tutorials.models import Tutorial, TutorialArticle
from tutorials.serializers import TutorialArticlePreviewSerializer, TutorialSerializer


class SearchEngine:
    def __init__(self):
        self.vector = SearchVector('title', 'preview')
        self.text_vector = SearchVector('text')
        self.articles = Article.objects.filter(published=True)
        self.tutorial_articles = TutorialArticle.objects.filter(published=True)
        self.tutorials = Tutorial.objects.filter(published=True)

    def search(self, query_string):
        start = SearchEngine._current_time()
        query_string = SearchEngine._normalize_query(query_string)
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        cached_value = redis_instance.get(query_string)
        if cached_value:
            cached_value = json.loads(cached_value)
            return {'time': SearchEngine._current_time() - start, 'results': cached_value}
        query = SearchQuery(query_string, search_type='phrase')
        articles_sr = self.articles.annotate(search=self.vector + self.text_vector).filter(search=query)
        articles_sr.annotate(rank=SearchRank(self.vector + self.text_vector, query)).order_by('-rank')
        tutorials_sr = self.tutorials.annotate(search=self.vector).filter(search=query)
        tutorials_sr.annotate(rank=SearchRank(self.vector, query)).order_by('-rank')
        tutorial_articles_sr = self.tutorial_articles.annotate(search=self.vector + self.text_vector).filter(
            search=query)
        tutorial_articles_sr.annotate(rank=SearchRank(self.vector + self.text_vector, query)).order_by('-rank')

        data = {
            'articles': ArticlePreviewSerializer(articles_sr, many=True).data,
            'tutorial_articles': TutorialArticlePreviewSerializer(tutorial_articles_sr, many=True).data,
            'tutorials': TutorialSerializer(tutorials_sr, many=True).data
        }
        redis_instance.set(query_string, json.dumps(data))
        redis_instance.expire(query_string, 60 * 30)  # cache lives 30 minutes
        return {'time': SearchEngine._current_time() - start, 'results': data}

    @staticmethod
    def _normalize_query(query: str):
        return ' '.join(sorted([word.lower() for word in query.strip().split()]))

    @staticmethod
    def _current_time():
        return int(round(time.time() * 1000))
