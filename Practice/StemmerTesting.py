from SourceFiles.KirilStemmer import KirilStemmer

tokens = ["angry","disappoint","quality", "meetings", "caresses", "ponies", "ties", "caress", "cats", "feed", "agreed", "disabled", "matting", "mating",
          "meeting", "milling", "messing"]
stems = []
stemmer = KirilStemmer()
for i in range(len(tokens)):
    stem = ""
    stem = stemmer.stemOneWord(tokens[i])
    stems.append(stem)

print(stems)
