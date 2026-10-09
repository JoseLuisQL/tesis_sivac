import win32com.client

while True:
    try:
        w = win32com.client.GetActiveObject("Word.Application")
        print("Found active Word application:", w)
        try:
            for doc in list(w.Documents):
                print("Closing doc:", doc.Name)
                doc.Close(SaveChanges=0)
        except Exception as e:
            print("Error closing docs:", e)
        w.Quit()
        print("Quit Word instance.")
    except Exception as e:
        print("No more active Word objects via GetActiveObject:", e)
        break
