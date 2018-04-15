import xlrd
import xlwt

NRC = xlrd.open_workbook("ResourceFiles/NRC.xlsx")
sheet = NRC.sheet_by_index(0)

affin = xlrd.open_workbook("ResourceFiles/AFINN-111.xlsx")
sheetaffin = affin.sheet_by_index(0)

NRC_new = xlwt.Workbook(encoding="utf-8")
newsheet = NRC_new.add_sheet("sheet1")

count = -1
for rowidx in range(1, sheet.nrows):
    row = sheet.row(rowidx)
    for affinrowid in range(sheetaffin.nrows):
        affinrow = sheetaffin.row(affinrowid)
        if row[0].value == affinrow[0].value:
            count = count+1
            newsheet.write(count, 0, row[0].value)
            newsheet.write(count, 1, row[1].value)
            newsheet.write(count, 2, row[2].value)
            newsheet.write(count, 3, row[3].value)
            newsheet.write(count, 4, row[4].value)
            newsheet.write(count, 5, row[5].value)
            newsheet.write(count, 6, row[6].value)


NRC_new.save("OutputFiles/NRC_new.xls")
