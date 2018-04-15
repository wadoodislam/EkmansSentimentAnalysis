class WordValance:

    def __init__(self, string):
        self.word = {
            'Word': string,
            'valance': {'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0, 'surprise': 0}
        }

    def __str__(self):
        return self.word['Word']

    def add(self, value):
        for i in range(len(self.word['valance'])):
            if self.word['valance'][i] != 0:
                self.word['valance'][i] += value

    def neutralize(self):
        for i in range(len(self.word['valance'])):
            self.word['valance'][i] = 0

    def shift(self):
        pass

    def add_anger(self):
        self.word['valance']['anger'] += 5
