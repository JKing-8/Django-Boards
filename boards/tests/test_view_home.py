from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve
from boards.models import Board
from boards.views import home


class HomeTests(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Django', descript='Django Board')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_container_link_topics_link(self):
        board_topics_url = reverse('board_topics', kwargs={"pk": self.board.pk})
        self.assertContains(self.response, f'href="{board_topics_url}"')
