import re
from lxml import etree
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns = {'w': W}
T = r'C:\MisInvestigaciones\tesis\sivac\salidas\archivo\_plan_instrumentos\_tmp'
def clean(e):
    s = etree.tostring(e).decode()
    s = re.sub(r' xmlns:\w+="[^"]+"', '', s)
    s = re.sub(r' w14:\w+="[^"]+"| w:rsid\w*="[^"]+"', '', s)
    return s
b = etree.parse(T + r'\Format\word\document.xml').getroot().find('w:body', ns)
ps = [e for e in b if e.tag == '{%s}p' % W]
for i in (0, 4, 19, 25, 26, 88, 91, 93, 101, 102, 110, 111, 112, 114):
    print('--P%d' % i, clean(ps[i])[:1800])
tb = b.findall('w:tbl', ns)
print('--ROW0 tbl1', clean(tb[1].findall('w:tr', ns)[0])[:1500])
print('--ROW1 tbl1', clean(tb[1].findall('w:tr', ns)[1])[:2500])
print('--ROW1 rubric', clean(tb[0].findall('w:tr', ns)[1])[:2500])
# page breaks / sectPr types
for i, e in enumerate(b):
    if e.tag == '{%s}p' % W and e.find('.//w:br', ns) is not None:
        print('BR at body idx', i)
# numbering used
print(re.findall(r'w:numId w:val="(\d+)"', open(T + r'\Format\word\document.xml', encoding='utf8').read())[:20])
n = open(T + r'\Format\word\numbering.xml', encoding='utf8').read()
print(re.sub(r' xmlns:\w+="[^"]+"', '', n)[-1800:])
