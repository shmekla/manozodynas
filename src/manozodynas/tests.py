# encoding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from manozodynas.testutils import StatefulTesting
from manozodynas.models import Word, Translation
from django.test import Client


class IndexTestCase(StatefulTesting):
    def test_index_page(self):
        self.open(reverse('index'))
        self.assertStatusCode(200)


class LoginTestCase(StatefulTesting):

    fixtures = ['test_fixture.json']

    def test_login_page(self):
        self.open(reverse('login'))
        self.assertStatusCode(200)

    def test_good_login(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'test',
            'password': 'test',
        })
        self.assertStatusCode(302)

    def test_bad_login(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'bad',
            'password': 'bad',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')

    def test_no_input(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': '',
            'password': '',
        })
        self.assertStatusCode(200)
        self.selectMany('.errorlist')

    def test_no_username(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': '',
            'password': 'test',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')

    def test_no_password(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'test',
            'password': '',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')


class WordAddTest(StatefulTesting):
    def tw_add(self):
        words = Word.objects.all()
        self.assertFalse(words.filter(word='test-laurynas-budrys').exists())
        self.open(reverse('add'))
        self.selectForm('#add-form')
        self.submitForm({
            'word': 'test-laurynas-budrys',
        })
        self.assertStatusCode(302)
        self.assertTrue(words.filter(word='test-laurynas-budrys').exists())


class TranslationAddTest(StatefulTesting):
    def tt_add(self):
        client = Client()
        response = client.post(reverse('add'), {
            'word': 'translate-budrys'
        })
        self.assertEqual(response.status_code, 302)
        words = Word.objects.all()
        self.assertTrue(words.filter(word='translate-budrys').exists())
        test_word = words.get(word='translate-budrys')
        response = client.post("/" + str(test_word.id) + '/translation', {
            'translation': 'translate-budrys2',
        })
        self.assertEqual(response.status_code, 302)
        translation = Translation.objects.all()
        self.assertTrue(
                translation.filter(translation='translate-budrys2',
                                   word=test_word).exists()
        )



