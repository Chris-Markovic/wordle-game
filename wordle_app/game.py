from .models import Session, Statistics, Wordlist
from .api import DictionaryAPI

class WordleApp:
    def __init__(self, user):
        self.user = user
        self.api_client = DictionaryAPI()

    def start_new_game(self):
        word = self.api_client.get_target_word()
        definition = self.api_client.get_word_definition(word)
        Wordlist.objects.get_or_create(target_word=word, defaults={'word_definition': definition})
        session = Session.objects.create(user=self.user, target_word=word, word_definition=definition)
        Statistics.objects.get_or_create(user=self.user)
        return session

    