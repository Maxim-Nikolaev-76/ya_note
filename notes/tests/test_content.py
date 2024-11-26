from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from notes.forms import NoteForm


User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note_author = Note.objects.create(
            title='Заголовок1',
            text='Текст',
            author=cls.author
        )
        cls.note_reader = Note.objects.create(
            title='Заголовок2',
            text='Текст',
            author=cls.author
        )

    def test_add_edit_note_form(self):
        for name, kwargs in (
            ('notes:add', None),
            ('notes:edit', {'slug': self.note_author.slug})
        ):
            self.client.force_login(self.author)
            url = reverse(name, kwargs=kwargs)
            response = self.client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_in_list_for_author(self):
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        self.assertIn(self.note_author, response.context['object_list'])

    def test_note_not_in_list_for_not_author(self):
        self.client.force_login(self.reader)
        url = reverse('notes:list')
        response = self.client.get(url)
        self.assertNotIn(self.note_author, response.context['object_list'])
