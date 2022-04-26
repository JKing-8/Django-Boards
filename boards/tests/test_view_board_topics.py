from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve
from boards.models import Board
from boards.views import board_topics


class BoardTopicsTests(TestCase):
    def setUp(self) -> None:
        Board.objects.create(name='Django', descript='Django Test Board')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_view_resolves_board_topics_view(self):
        view = resolve('/boards/1')
        self.assertEquals(view.func, board_topics)

    def test_home_view_container_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, f'href="{homepage_url}"')

    def test_board_topics_view_contains_navigations_link(self):
        board_topic_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topics_url = reverse('new_topics', kwargs={'pk': 1})
        response = self.client.get(board_topic_url)
        self.assertContains(response, f'href="{homepage_url}"')
        self.assertContains(response, f'href="{new_topics_url}"')
