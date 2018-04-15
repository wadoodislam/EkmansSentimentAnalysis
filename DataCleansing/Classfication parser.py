import xml.etree.ElementTree as elementTree
import xlwt

tree = elementTree.parse("ResourceFiles/classification.xml")
root = tree.getroot()


def inthis(keyname, value, words, emotionname):
    for word in words:
        if keyname == word[0]:
            if emotionname == "anger":
                word[1] = value
            elif emotionname == "disgust":
                word[2] = value
            elif emotionname == "fear":
                word[3] = value
            elif emotionname == "joy":
                word[4] = value
            elif emotionname == "sadness":
                word[5] = value
            elif emotionname == "surprise":
                word[6] = value
            return True
    return False


# open a file for writing

Lexicon = xlwt.Workbook(encoding="utf-8")
sheet = Lexicon.add_sheet("sheet1")

words = []

for emotion in root.findall('emotion'):
    emotionname = emotion.get("name")
    for keyword in emotion.findall("keyword"):
        wordname = keyword.get("name")
        value = keyword.get("value")
        if not inthis(wordname, value, words, emotionname):
            if emotionname == "anger":
                words.append([wordname, value, 0, 0, 0, 0, 0])
            elif emotionname == "disgust":
                words.append([wordname, 0, value, 0, 0, 0, 0])
            elif emotionname == "fear":
                words.append([wordname, 0, 0, value, 0, 0, 0])
            elif emotionname == "joy":
                words.append([wordname, 0, 0, 0, value, 0, 0])
            elif emotionname == "sadness":
                words.append([wordname, 0, 0, 0, 0, value, 0])
            elif emotionname == "surprise":
                words.append([wordname, 0, 0, 0, 0, 0, value])

for keyword in root.findall('keyword'):
    name = keyword.get("name")
    flag = False
    for word in words:
        if word[0] == name:
            flag = True
    if not flag:
        flag = True
count = 0
for word in words:
    sheet.write(count, 0, word[0])
    sheet.write(count, 1, int(word[1]))
    sheet.write(count, 2, int(word[2]))
    sheet.write(count, 3, int(word[3]))
    sheet.write(count, 4, int(word[4]))
    sheet.write(count, 5, int(word[5]))
    sheet.write(count, 6, int(word[6]))
    count += 1

Lexicon.save("OutputFiles/Lexicon.xls")
