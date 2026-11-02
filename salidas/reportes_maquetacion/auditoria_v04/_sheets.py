import os
from PIL import Image, ImageDraw
base = r"C:\MisInvestigaciones\tesis\sivac\salidas\reportes_maquetacion\auditoria_v04"
files = sorted(f for f in os.listdir(base) if f.startswith("p") and f.endswith(".png"))
os.makedirs(os.path.join(base,"sheets"), exist_ok=True)
per = 6  # 3 cols x 2 rows
thumb_w = 600
for s in range(0, len(files), per):
    chunk = files[s:s+per]
    ims=[]
    for f in chunk:
        im = Image.open(os.path.join(base,f))
        r = thumb_w/im.width
        im = im.resize((thumb_w, int(im.height*r)), Image.LANCZOS)
        ims.append((f,im))
    W = thumb_w*3 + 40
    H = max(i.height for _,i in ims)*2 + 60
    sheet = Image.new("RGB",(W,H),"white")
    for k,(f,im) in enumerate(ims):
        x = 10 + (k%3)*(thumb_w+10)
        y = 10 + (k//3)*(im.height+20)
        sheet.paste(im,(x,y))
        d=ImageDraw.Draw(sheet)
        d.rectangle([x,y,x+thumb_w-1,y+im.height-1],outline="red",width=2)
    out = os.path.join(base,"sheets",f"sheet_{s//per+1:02d}_{chunk[0][:-4]}_{chunk[-1][:-4]}.jpg")
    sheet.save(out, quality=82)
    print(out)
