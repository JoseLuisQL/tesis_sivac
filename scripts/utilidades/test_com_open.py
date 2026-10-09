import os
import win32com.client

test_docx = os.path.abspath("salidas/documentos/test_sample.docx")
import docx
d = docx.Document()
d.add_paragraph("Hello world")
d.save(test_docx)

# Test COM
try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(test_docx)
    print("Opened successfully:", doc.Name)
    print("Paragraphs count:", doc.Paragraphs.Count)
    doc.Close(False)
    word.Quit()
    print("Closed successfully!")
except Exception as e:
    print("COM Error:", e)
