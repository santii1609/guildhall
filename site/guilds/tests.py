from django.test import TestCase
from django.utils import timezone
from django.urls import reverse


import datetime

from .models import Guild


# Create your tests here.
class GuildModelTests(TestCase):


    def test_testing_github(self):
        testResult = True
        self.assertIs(testResult, False)


    def test_was_created_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose creation_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        guild = Guild(creation_date=time)

        self.assertIs(guild.was_created_recently(), False)


    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose creation_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        guild = Guild(creation_date=time)
        self.assertIs(guild.was_created_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose creation_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        guild = Guild(creation_date=time)
        self.assertIs(guild.was_created_recently(), True)


def create_guild(name, days):

    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Guild.objects.create(name=name, creation_date=time)


class GuildIndexViewTests(TestCase):


    def test_no_guilds(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('guilds:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No guilds are available.")
        self.assertQuerysetEqual(response.context['guilds'], [])

    def test_past_guild(self):
        """
        Questions with a creation_date in the past are displayed on the
        index page.
        """
        create_guild(name="Past question.", days=-30)
        response = self.client.get(reverse('guilds:index'))
        self.assertQuerysetEqual(
            response.context['guilds'],
            ['<Guild: Past question.>']
        )

    def test_future_guild(self):
        """
        Questions with a creation_date in the future aren't displayed on
        the index page.
        """
        create_guild(name="Future question.", days=30)
        response = self.client.get(reverse('guilds:index'))
        self.assertContains(response, "No guilds are available.")
        self.assertQuerysetEqual(response.context['guilds'], [])

    def test_future_guild_and_past_guild(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_guild(name="Past question.", days=-30)
        create_guild(name="Future question.", days=30)
        response = self.client.get(reverse('guilds:index'))
        self.assertQuerysetEqual(
            response.context['guilds'],
            ['<Guild: Past question.>']
        )

    def test_two_past_guilds(self):
        """
        The questions index page may display multiple questions.
        """
        create_guild(name="Past question 1.", days=-30)
        create_guild(name="Past question 2.", days=-5)
        response = self.client.get(reverse('guilds:index'))
        self.assertQuerysetEqual(
            response.context['guilds'],
            ['<Guild: Past question 2.>', '<Guild: Past question 1.>']
        )



class GuildDetailViewTests(TestCase):

    def test_future_guild(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        guild = create_guild(name='Future question.', days=5)
        url = reverse('guilds:detail', args=(guild.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_guild(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        guild = create_guild(name='Past Question.', days=-5)
        url = reverse('guilds:detail', args=(guild.id,))
        response = self.client.get(url)
        self.assertContains(response, guild.name)

