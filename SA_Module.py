# Importing natural language processing toolkit
import nltk
# Importing excel file reader
import xlrd
# Importing sentence and word tokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
# Importing word stemmer
from KirilStemmer import KirilStemmer
# Importing WordNet Lemmatizer
from nltk.stem import WordNetLemmatizer
# Importing WordNet
from nltk.corpus import wordnet as wn
# Importing WordProfile
from WordProfile import WordValance

# Opening NRC word-emotion relation lexicon
LEX = xlrd.open_workbook("Output Files/Lexicon.xls")
LEX_sheet = LEX.sheet_by_index(0)


class SentimentAnalysis:
    # Word filter tags
    __filter_tags = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP',
                     'NNP$', 'RB', 'RBR', 'RBS', 'VB', 'VBD',
                     'VBG', 'VBN', 'VBP', 'VBZ']

    def __init__(self):
        self.valance = {'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0, 'surprise': 0}

    #   def phraseDetect(self, text):

    def analyze(self, text):
        # sentence tokenization
        sentences = sent_tokenize(text)
        for sentence in sentences:
            self.__sentence_process(sentence)

    def __sentence_process(self, sentence):
        # word tokenization
        words = word_tokenize(sentence)
        # Parts of speech tagging
        words = nltk.pos_tag(words)
        words = self.__word_filter(words)
        words = self.__base_form(words)
        words = self.__stem(words)
        affective_words = self.detect_affective(words)

    @staticmethod
    def detect_affective(words):
        affective_words = []
        for word in words:
            for rowid in range(LEX_sheet.nrows):
                row = LEX_sheet.row(rowid)
                if word == row[0].value:
                    w_valance = WordValance(word)
                    w_valance.word['valance'] = {
                        'anger': row[1].value,
                        'disgust': row[2].value,
                        'fear': row[3].value,
                        'joy': row[4].value,
                        'sadness': row[5].value,
                        'surprise': row[6].value
                    }
                    affective_words.append(w_valance)
        return affective_words

    @staticmethod
    def __stem(words):
        stemmer = KirilStemmer()
        stem_words = []
        for word in words:
            stem_words.append(stemmer.stemOneWord(word))
        return stem_words

    @staticmethod
    def __base_form(words):
        wnl = WordNetLemmatizer()
        base_words = []
        for word in words:
            if word[1] == 'NN' or word[1] == 'NNS' or word[1] == 'NNP' or word[1] == 'NNP$':
                temp = wnl.lemmatize(word[0], wn.NOUN)
                base_words.append(temp)
            elif word[1] == 'VB' or word[1] == 'VBD' or word[1] == 'VBG' or word[1] == 'VBN' or word[1] == 'VBP' or word[1] == 'VBZ':
                temp = wnl.lemmatize(word[0], wn.VERB)
                base_words.append(temp)
            elif word[1] == 'RB' or word[1] == 'RBR' or word[1] == 'RBS':
                temp = wnl.lemmatize(word[0], wn.ADV)
                base_words.append(temp)
            elif word[1] == 'JJ' or word[1] == 'JJR' or word[1] == 'JJS':
                temp = wnl.lemmatize(word[0], wn.ADJ)
                base_words.append(temp)
        return base_words

    def __word_filter(self, words):
        filtered_words = []
        for pos in words:
            if pos[1] in self.__filter_tags:
                filtered_words.append(pos)
        return filtered_words


# dummy text
example_text = "I was disappointed and angry at the bad quality of a documentary program on TV. In my opinion, " \
               "the topic was important and the program should have been made with seriousness and consideration."
SA = SentimentAnalysis()
SA.analyze(example_text)
