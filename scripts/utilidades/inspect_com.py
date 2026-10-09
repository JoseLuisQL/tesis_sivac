import os
import win32com.client

word = win32com.client.Dispatch("Word.Application")
print("word.Documents:", type(word.Documents), dir(word.Documents))
print("Open member:", word.Documents._oleobj_.GetIDsOfNames("Open"))
doc = word.Documents.Open(os.path.abspath("salidas/documentos/test_sample.docx"))
print("doc type:", type(doc))
print("doc repr:", repr(doc))
word.Quit()
