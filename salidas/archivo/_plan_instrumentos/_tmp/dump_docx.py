import sys, re
from lxml import etree
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns = {'w': W}
q = lambda t: '{%s}%s' % (W, t)

def rpr(r):
    p = r.find('w:rPr', ns)
    if p is None:
        return ''
    out = []
    for t in ('b', 'i', 'u', 'caps', 'smallCaps'):
        e = p.find('w:' + t, ns)
        if e is not None and e.get(q('val')) not in ('0', 'false'):
            out.append(t)
    f = p.find('w:rFonts', ns)
    if f is not None:
        out.append('f=' + (f.get(q('ascii')) or f.get(q('hAnsi')) or ''))
    s = p.find('w:sz', ns)
    if s is not None:
        out.append('sz=' + s.get(q('val')))
    c = p.find('w:color', ns)
    if c is not None:
        out.append('c=' + c.get(q('val')))
    h = p.find('w:highlight', ns)
    if h is not None:
        out.append('hl=' + h.get(q('val')))
    return ','.join(out)

def ptxt(p):
    segs = []
    for r in p.iter(q('r')):
        t = ''
        for c in r:
            if c.tag == q('t'):
                t += c.text or ''
            elif c.tag == q('tab'):
                t += '\\t'
            elif c.tag == q('br'):
                t += '\\n[br:%s]' % (c.get(q('type')) or 'line')
            elif c.tag == q('drawing') or c.tag == q('pict'):
                t += '[IMG]'
            elif c.tag == q('sym'):
                t += '[SYM %s]' % c.get(q('char'))
        if t:
            segs.append((rpr(r), t))
    return segs

def pprop(p):
    pp = p.find('w:pPr', ns)
    if pp is None:
        return ''
    out = []
    st = pp.find('w:pStyle', ns)
    if st is not None:
        out.append('style=' + st.get(q('val')))
    j = pp.find('w:jc', ns)
    if j is not None:
        out.append('jc=' + j.get(q('val')))
    ind = pp.find('w:ind', ns)
    if ind is not None:
        out.append('ind=' + ','.join('%s:%s' % (k.split('}')[1], v) for k, v in ind.attrib.items()))
    sp = pp.find('w:spacing', ns)
    if sp is not None:
        out.append('sp=' + ','.join('%s:%s' % (k.split('}')[1], v) for k, v in sp.attrib.items()))
    if pp.find('w:numPr', ns) is not None:
        out.append('num')
    if pp.find('w:sectPr', ns) is not None:
        out.append('SECTPR')
    return ' '.join(out)

def sect(s):
    o = []
    for t in ('pgSz', 'pgMar', 'cols', 'headerReference', 'footerReference', 'type', 'titlePg', 'pgNumType'):
        for e in s.findall('w:' + t, ns):
            o.append(t + '{' + ','.join('%s=%s' % (k.split('}')[1], v) for k, v in e.attrib.items()) + '}')
    return ' '.join(o)

def tblinfo(t):
    pr = t.find('w:tblPr', ns)
    o = []
    if pr is not None:
        for e in pr:
            o.append(e.tag.split('}')[1] + '{' + ','.join('%s=%s' % (k.split('}')[1], v) for k, v in e.attrib.items()) + '}')
    g = t.find('w:tblGrid', ns)
    cols = [c.get(q('w')) for c in g.findall('w:gridCol', ns)] if g is not None else []
    return ' '.join(o), cols

def cellinfo(tc):
    pr = tc.find('w:tcPr', ns)
    o = []
    if pr is not None:
        for e in pr:
            n = e.tag.split('}')[1]
            if n == 'tcBorders':
                o.append('borders')
            else:
                o.append(n + '{' + ','.join('%s=%s' % (k.split('}')[1], v) for k, v in e.attrib.items()) + '}')
    return ' '.join(o)

def dump(path, maxrows=None):
    tree = etree.parse(path)
    body = tree.getroot().find('w:body', ns)
    i = 0
    for el in body:
        if el.tag == q('p'):
            segs = ptxt(el)
            txt = ''.join(s[1] for s in segs)
            fm = sorted(set(s[0] for s in segs))
            print('P%03d [%s] %s | %s | %s' % (i, pprop(el), txt, ' ; '.join(fm), ''))
            i += 1
        elif el.tag == q('tbl'):
            info, cols = tblinfo(el)
            rows = el.findall('w:tr', ns)
            print('TABLE rows=%d cols=%s\n  tblPr: %s' % (len(rows), cols, info))
            for ri, tr in enumerate(rows):
                trp = tr.find('w:trPr', ns)
                trs = ''
                if trp is not None:
                    trs = ' '.join(e.tag.split('}')[1] + '{' + ','.join('%s=%s' % (k.split('}')[1], v) for k, v in e.attrib.items()) + '}' for e in trp)
                if maxrows is None or ri < maxrows or ri >= len(rows) - 1:
                    print('  ROW%d trPr:%s' % (ri, trs))
                    for ci, tc in enumerate(tr.findall('w:tc', ns)):
                        txt = ' // '.join(''.join(s[1] for s in ptxt(p)) for p in tc.findall('w:p', ns))
                        fm = sorted(set(s[0] for pp in tc.findall('w:p', ns) for s in ptxt(pp)))
                        pj = [pprop(pp) for pp in tc.findall('w:p', ns)][:1]
                        print('    C%d [%s] {%s} %s | %s' % (ci, cellinfo(tc), pj[0] if pj else '', txt, ' ; '.join(fm)))
            print('ENDTABLE')
        elif el.tag == q('sectPr'):
            print('FINAL SECTPR', sect(el))
        else:
            print('OTHER', el.tag)
    # inner sections
    for s in body.iter(q('sectPr')):
        print('SECT:', sect(s))

if __name__ == '__main__':
    dump(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)
