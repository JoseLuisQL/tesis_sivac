import sys, re
from lxml import etree
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns = {'w': W}
T = r'C:\MisInvestigaciones\tesis\sivac\salidas\archivo\_plan_instrumentos\_tmp'
for d in ('Format', 'CORREC'):
    print('=====', d)
    s = etree.parse(T + '\\' + d + r'\word\styles.xml').getroot()
    dd = s.find('w:docDefaults', ns)
    print('docDefaults', re.sub(r' xmlns:\w+="[^"]+"', '', etree.tostring(dd).decode()))
    for st in s.findall('w:style', ns):
        sid = st.get('{%s}styleId' % W)
        if sid in ('Normal', 'Textoindependiente', 'Prrafodelista', 'Ttulo1', 'TableParagraph', 'Tablaconcuadrcula', 'TableNormal'):
            print(sid, re.sub(r' xmlns:\w+="[^"]+"', '', etree.tostring(st).decode()))
    print('FONTTABLE', re.findall(r'w:name="([^"]+)"', open(T + '\\' + d + r'\word\fontTable.xml', encoding='utf8').read()))
    n = open(T + '\\' + d + r'\word\numbering.xml', encoding='utf8').read()
    print('NUMBERING', re.sub(r' xmlns:\w+="[^"]+"', '', n)[:3500])
    print('SETTINGS', re.sub(r' xmlns:\w+="[^"]+"', '', open(T + '\\' + d + r'\word\settings.xml', encoding='utf8').read())[:2500])
    print('CORE', open(T + '\\' + d + r'\docProps\core.xml', encoding='utf8').read()[-500:])
    print('APP', open(T + '\\' + d + r'\docProps\app.xml', encoding='utf8').read()[-700:])
    print('RELS', open(T + '\\' + d + r'\word\_rels\document.xml.rels', encoding='utf8').read())
