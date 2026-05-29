import requests, random


class DictionaryAPI:
    def __init__(self):
        self.dictionary_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        self.random_word_url = "https://api.datamuse.com/words?sp=?????&max=500&topics=common"

    def get_target_word(self):
        response = requests.get(self.random_word_url, timeout=5)
        words = response.json()
        random.shuffle(words)
        for entry in words:
            word = entry["word"]
            if self.check_word_exists(word):
                return word.upper()


        backup_words = ["plane", "leave", "plead", "plant", "stone"]
        return random.choice(backup_words).upper()

    def check_word_exists(self, word):
        response = requests.get(self.dictionary_url + word, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False

    def get_word_definition(self, word):
        try:
            response = requests.get(self.dictionary_url + word, timeout=5)
            data = response.json()
            return data[0]['meanings'][0]['definitions'][0]['definition']
        except:
            return "No definition found."

get_word = DictionaryAPI()
target_word = get_word.get_target_word()
print(target_word)
print(get_word.get_word_definition(target_word))
