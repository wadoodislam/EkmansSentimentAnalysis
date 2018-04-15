# Importing natural language processing toolkit
import nltk
# Importing excel file reader
import xlrd
# Importing sentence and word tokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
# Importing word stemmer
from nltk.stem.snowball import SnowballStemmer

# Opening AFFIN lexicon worksheet
AFFIN = xlrd.open_workbook("ResourceFiles/AFINN-111.xlsx")
AFFIN_sheet = AFFIN.sheet_by_index(0)
# Opening NRC word-emotion relation lexicon
NRC = xlrd.open_workbook("OutputFiles/NRC_new.xls")
NRC_sheet = NRC.sheet_by_index(0)

# Word filter tags
filter_tags = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP',
               'NNP$', 'RB', 'RBR', 'RBS', 'VB', 'VBD',
               'VBG', 'VBN', 'VBP', 'VBZ']

# dummy text
example_text = "But instead if you work hard I will give you reward and some bonus as well in the form of money. " \
               "The sky is pinkish-blue. You should not eat cardboard."


# Returns the newly mapped valance of a word
def valance(word):
    for rowid in range(AFFIN_sheet.nrows):
        row = AFFIN_sheet.row(rowid)
        if row[0].value == word:
            return 5 + 3 * abs(row[1].value)
    return 0


# Lexicon based algorithm
def emotion_detection(user_text):
    # initializing stemmer with english language
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    # sentence tokenization
    sentences = sent_tokenize(user_text)
    # sentence level analysis
    for s in sentences:
        filtered_words = []
        # word tokenization
        words = word_tokenize(s)
        # Parts of speech tagging
        pos_words = nltk.pos_tag(words)
        for pos in pos_words:
            if pos[1] in filter_tags:
                filtered_words.append(pos[0])
        print(filtered_words)
        stemmed_words = []
        for w in filtered_words:
            stemmed_words.append(stemmer.stem(w))
        print(stemmed_words)
        word_tuples = []
        for word in stemmed_words:
            for rowid in range(NRC_sheet.nrows):
                row = NRC_sheet.row(rowid)
                if word == row[0].value:
                    valances = [0, 0, 0, 0, 0, 0]
                    value = valance(word)
                    if value > 0:
                        for i in range(6):
                            if row[i].value == 1:
                                valances[i-1] = value
                        word_tuples.append({
                            "word": word,
                            "valances": valances
                        })
        print(word_tuples)
        final = {
            "Anger": 0,
            "Disgust": 0,
            "Fear": 0,
            "Joy": 0,
            "Sadness": 0,
            "Surprise": 0
        }
        for wt in word_tuples:
            valances = wt["valances"]
            final["Anger"] += valances[0]
            final["Disgust"] += valances[1]
            final["Fear"] += valances[2]
            final["Joy"] += valances[3]
            final["Sadness"] += valances[4]
            final["Surprise"] += valances[5]
        return final


emotion_detection(example_text)
