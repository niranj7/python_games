import json, random, os

class WordManager:
    def __init__(self, json_path, images_folder):
        with open(json_path, "r") as f:
            self.words = json.load(f)
        self.images_folder = images_folder
        self.keys = list(self.words.keys())

    def get_random(self):
        word = random.choice(self.keys)
        img_file = self.words[word]
        img_path = os.path.join(self.images_folder, img_file)
        snippet = self.make_snippet(word)
        return word, img_path, snippet

    def make_snippet(self, word):
        if len(word) <= 2:
            return word
        # show first and last letter, hide middle as underscores about he letter 
        return " ".join([word[0]] + ["_"]*(len(word)-2) + [word[-1]])