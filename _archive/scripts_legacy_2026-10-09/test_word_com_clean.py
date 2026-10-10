import os
import win32com.client

test_docx = os.path.abspath("salidas/documentos/test_toc.docx")
print("Opening word...")
word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0 # wdAlertsNone

try:
    print("Opening doc...")
    doc = word.Documents.Open(FileName=test_docx, ReadOnly=False)
    print("Doc type:", type(doc))
    print("Doc name:", doc.Name)
    print("TOC count:", doc.TablesOfContents.Count)
    print("Fields count:", doc.Fields.Count)

    # Updating TOCs
    for i in range(1, doc.TablesOfContents.Count + 1):
        print(f"Updating TOC {i}...")
        doc.TablesOfContents.Item(i).Update()

    # Updating Fields
    print("Updating fields...")
    for i in range(1, doc.Fields.Count + 1):
        try:
            doc.Fields.Item(i).Update()
        except Exception as e:
            print(f"Field {i} update error: {e}")

    doc.Save()
    print("Saved doc!")
    doc.Close(SaveChanges=0)
finally:
    word.Quit()
    print("Word quit successfully.")
