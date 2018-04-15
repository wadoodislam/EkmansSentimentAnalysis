class TextValance:

    def __init__(self, string):
        self.profile = {
            'text': string,
            'valance': {'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0, 'surprise': 0}
        }

    def __str__(self):
        return self.profile['Word']

    def add(self, value):
        for i in range(len(self.word['valance'])):
            if self.profile['valance'][i] != 0:
                self.profile['valance'][i] += value

    def neutralize(self):
        for i in range(len(self.word['valance'])):
            self.profile['valance'][i] = 0

    def shift(self):
        pass

    def add_anger(self):
        self.profile['valance']['anger'] += 5
