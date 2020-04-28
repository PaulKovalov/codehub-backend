# Create your tests here.
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from tutorials.models import Tutorial, TutorialArticle, TutorialArticleComment, TutorialArticleCommentReaction, \
    TutorialArticleReaction
from tutorials.serializers import TutorialArticlePreviewSerializer, TutorialSerializer, \
    MyTutorialSerializer, TutorialArticleCommentSerializer


class TestTutorials(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.author = mommy.make(User)
        self.tutorial = mommy.make(Tutorial, author=self.author)

    def test_tutorials_list(self):
        url = reverse('tutorials-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tutorial_create(self):
        url = reverse('tutorials-list')
        self.client.force_authenticate(self.author)
        data = {
            'title': 'A title of the tutorial',
            'preview': 'Preview of the tutorial'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tutorial_retrieve(self):
        tutorial = mommy.make(Tutorial, published=True, views=10)
        url = reverse('tutorials-detail', kwargs={'pk': tutorial.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], tutorial.id)
        self.assertEqual(Tutorial.objects.get(id=tutorial.id).views, 11)

    def test_tutorial_edit(self):
        self.client.force_authenticate(self.author)
        url = reverse('tutorials-detail', kwargs={'pk': self.tutorial.id})
        data = {
            'title': 'New title',
            'preview': 'New preview'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tutorial.objects.get(id=response.json()['id']).title, data['title'])
        self.assertEqual(Tutorial.objects.get(id=response.json()['id']).preview, data['preview'])

    def test_my_tutorials_list(self):
        another_tutorial = mommy.make(Tutorial)
        url = reverse('tutorials-my')
        self.client.force_authenticate(self.author)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(MyTutorialSerializer(another_tutorial).data not in response.json()['results'])
        self.assertTrue(MyTutorialSerializer(self.tutorial).data in response.json()['results'])

    def test_non_published_tutorial_retrieve_by_author(self):
        url = reverse('tutorials-detail', kwargs={'pk': self.tutorial.id})
        self.client.force_authenticate(self.author)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), TutorialSerializer(self.tutorial).data)

    def test_recent_tutorials(self):
        num_of_tutorials = 5
        tutorials = mommy.make(Tutorial, _quantity=num_of_tutorials, published=True)
        url = reverse('tutorials-recent')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for tutorial in tutorials:
            self.assertTrue(TutorialSerializer(tutorial).data in response.json())


class TestTutorialArticles(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.author = mommy.make(User)
        self.tutorial = mommy.make(Tutorial, author=self.author)

    def test_tutorial_article_create(self):
        url = reverse('tutorial-articles-list', kwargs={'tutorial_pk': self.tutorial.pk})
        data = {
            'text': 'random text here' * 10,
            'title': 'some title here'
        }
        self.client.force_authenticate(self.author)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['tutorial'], self.tutorial.id)
        self.assertTrue(TutorialArticle.objects.filter(id=response.json()['id']))

    def test_tutorial_article_retrieve(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=True, tutorial=self.tutorial,
                                      views=10)
        url = reverse('tutorial-articles-detail', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': tutorial_article.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tutorial_article.id, response.json()['id'])
        self.assertEqual(TutorialArticle.objects.get(id=tutorial_article.id).views, 11)

    def test_tutorial_articles_list(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=True, tutorial=self.tutorial)
        url = reverse('tutorial-articles-list', kwargs={'tutorial_pk': self.tutorial.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'][0], TutorialArticlePreviewSerializer(tutorial_article).data)

    def test_tutorial_article_publish_user(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=False, tutorial=self.tutorial)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial-articles-detail', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': tutorial_article.pk})
        data = {
            'published': True
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_non_published_tutorial_article(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=False, tutorial=self.tutorial)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial-articles-detail', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': tutorial_article.pk})
        data = {
            'text': 'new text here' * 5
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TutorialArticle.objects.get(id=response.json()['id']).text, data['text'])

    def test_edit_published_tutorial_article(self):
        tutorial_article = mommy.make(TutorialArticle, author=self.author, published=True, tutorial=self.tutorial)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial-articles-detail', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': tutorial_article.pk})
        data = {
            'text': 'new text here' * 5
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TutorialArticle.objects.get(id=response.json()['id']).text, data['text'])

    def test_like_tutorial_article(self):
        article = mommy.make(TutorialArticle, author=self.author, published=True, tutorial=self.tutorial)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial-articles-like', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': article.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TutorialArticleReaction.objects.get(article__id=article.id, type='like'), 1)

    def test_dislike_tutorial_article(self):
        article = mommy.make(TutorialArticle, author=self.author, published=True, tutorial=self.tutorial)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial-articles-dislike', kwargs={'tutorial_pk': self.tutorial.pk, 'pk': article.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TutorialArticleReaction.objects.get(article__id=article.id, type='dislike'), 1)


class TestArticleComments(TestCase):
    def setUp(self) -> None:
        self.author = mommy.make(User)
        self.random_user = mommy.make(User)
        self.tutorial = mommy.make(Tutorial, author=self.author, published=True)
        self.article = mommy.make(TutorialArticle, tutorial=self.tutorial, author=self.author)
        self.published_article = mommy.make(TutorialArticle, tutorial=self.tutorial, author=self.author, published=True)
        self.client = APIClient()

    @patch('tutorials.views.send_mail_on_new_comment')
    def test_comment_create(self, mocked_send_email):
        self.client.force_authenticate(self.random_user)
        url = reverse('tutorial_article-comments-list',
                      kwargs={'tutorial_pk': self.tutorial.pk, 'article_pk': self.published_article.id})
        data = {
            'text': 'Some comment text',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_comment = TutorialArticleComment.objects.get(id=response.json()['id'])
        mocked_send_email.assert_called_once_with(self.published_article.author.email, self.random_user,
                                                  created_comment)

    def test_comment_create_non_published_article(self):
        self.client.force_authenticate(self.random_user)
        url = reverse('tutorial_article-comments-list',
                      kwargs={'tutorial_pk': self.tutorial.pk, 'article_pk': self.article.id})
        data = {
            'text': 'Some comment text',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comments_list(self):
        num_of_comments = 6
        comments = mommy.make(TutorialArticleComment, _quantity=num_of_comments, author=self.random_user,
                              article=self.published_article)
        url = reverse('tutorial_article-comments-list',
                      kwargs={'tutorial_pk': self.tutorial.pk, 'article_pk': self.published_article.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for comment in comments:
            self.assertTrue(TutorialArticleCommentSerializer(comment).data in response.json()['results'])

    def test_comments_edit(self):
        comment = mommy.make(TutorialArticleComment, author=self.random_user, article=self.published_article)
        self.client.force_authenticate(self.random_user)
        url = reverse('tutorial_article-comments-detail',
                      kwargs={'tutorial_pk': self.tutorial.pk, 'article_pk': self.published_article.id,
                              'pk': comment.pk})
        data = {
            'text': 'New text for the comment'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TutorialArticleComment.objects.get(id=comment.id).text, data['text'])

    def test_comment_reply(self):
        comment = mommy.make(TutorialArticleComment, author=self.random_user, article=self.published_article)
        self.client.force_authenticate(self.random_user)
        url = reverse('tutorial_article-comments-list',
                      kwargs={'tutorial_pk': self.tutorial.pk, 'article_pk': self.published_article.id})
        data = {
            'text': 'New text for the comment',
            'reply_to': comment.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            response.json()['id'] in TutorialArticleComment.objects.get(id=comment.id).replies.values_list('id',
                                                                                                           flat=True))

    def test_comment_reaction_like(self):
        comment = mommy.make(TutorialArticleComment, author=self.random_user, article=self.published_article)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial_article-comments-like',
                      kwargs={'tutorial_pk': self.tutorial.pk, 'article_pk': self.published_article.id,
                              'pk': comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TutorialArticleCommentReaction.objects.filter(comment__id=comment.id, type='like'), 1)

    def test_comment_reaction_dislike(self):
        comment = mommy.make(TutorialArticleComment, author=self.random_user, article=self.published_article)
        self.client.force_authenticate(self.author)
        url = reverse('tutorial_article-comments-dislike',
                      kwargs={'tutorial_pk': self.tutorial.pk, 'article_pk': self.published_article.id,
                              'pk': comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TutorialArticleCommentReaction.objects.filter(comment__id=comment.id, type='dislike'), 1)
