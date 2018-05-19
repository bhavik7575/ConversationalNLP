import pandas as pd
from collections import Counter
import xlsxwriter
import openpyxl
from xlrd import open_workbook
from xlutils.copy import copy
import json

writer = pd.ExcelFile('ConversationLogs.xlsx')

print(type(writer))
print(writer)

print(writer.sheet_names)

df=writer.parse("ConversationLogs")

df=df["Response"]
#df=df[0:9]

mat=df.as_matrix()

print(type(mat))

print(mat.shape[0])

xfile = openpyxl.load_workbook('ConversationLogs.xlsx')

sheet = xfile.get_sheet_by_name('ConversationLogs')
for i in range(0,mat.shape[0]):
    jsondata=df[i]
    print(jsondata)
    dictVar = json.loads(jsondata)
    print(dictVar)
    dictVar=dict(dictVar['intents'][0])
    print(dictVar.get('intent'))
    txt=str(dictVar.get('intent'))
    Id = "D" + str(i + 2)
    sheet[Id]=txt


xfile.save('ConversationLogs1.xlsx')
