import xml.etree.ElementTree as elementTree
import xlwt

tree = elementTree.parse("ResourceFiles/phrases.xml")
root = tree.getroot()

# open a file for writing

Lexicon = xlwt.Workbook(encoding="utf-8")
sheet = Lexicon.add_sheet("sheet1")

count = 0
for phrase in root.findall('phrase'):
    name = phrase.get("name")
    text = phrase.text
    sheet.write(count, 0, name)
    sheet.write(count, 1, text)
    count += 1

Lexicon.save("OutputFiles/Phrases.xls")
