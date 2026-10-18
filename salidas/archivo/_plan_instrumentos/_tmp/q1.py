import sys
sys.path.insert(0, r'C:\MisInvestigaciones\tesis\sivac\salidas\archivo\_plan_instrumentos\_tmp')
from dump_docx import *
T = r'C:\MisInvestigaciones\tesis\sivac\salidas\archivo\_plan_instrumentos\_tmp'
def tx(p): return ''.join(s[1] for s in ptxt(p))

t = etree.parse(T + r'\Format\word\document.xml')
tbls = t.getroot().findall('.//w:tbl', ns)
print('RUBRIC row4:')
for tc in tbls[0].findall('w:tr', ns)[4].findall('w:tc', ns):
    print(' // '.join(tx(p) for p in tc.findall('w:p', ns)))
print('RUBRIC row 5 detail pj:')
for ti, tb in enumerate(tbls):
    print('TABLE', ti, 'rows', len(tb.findall('w:tr', ns)))
for ti in (1, 2):
    print('ITEMS tbl', ti)
    for tr in tbls[ti].findall('w:tr', ns)[1:]:
        tcs = tr.findall('w:tc', ns)
        print(tx(tcs[0].find('w:p', ns)), '|', ' '.join(tx(p) for p in tcs[1].findall('w:p', ns)))

# borders of tbl 1
b = tbls[1].find('w:tblPr', ns)
print(etree.tostring(b).decode()[-600:])
tc = tbls[1].findall('w:tr', ns)[0].find('w:tc', ns)
print(etree.tostring(tc.find('w:tcPr', ns)).decode()[-500:])
tc = tbls[0].findall('w:tr', ns)[0].find('w:tc', ns)
print('RUBRIC tcPr', etree.tostring(tc.find('w:tcPr', ns)).decode()[-700:])
print(etree.tostring(tbls[0].find('w:tblPr', ns)).decode()[-900:])
