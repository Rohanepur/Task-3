#!/usr/bin/env python3
"""Filing fetch/verify + entry inspector helper for remediation agents.
Usage:
  python3 agent_tools/fv.py show <rec> <ann>            # dump full entry
  python3 agent_tools/fv.py find <rec> "needle" ["n2" ...]  # list physical pages containing each needle
  python3 agent_tools/fv.py page <rec> <physical_page>  # dump text of one physical page
  python3 agent_tools/fv.py around <rec> <physical_page> "needle" [before] [after]
Note: metadata page_numbers are PRINTED pages; physical index is usually printed-1.
"""
import json, sys, hashlib, os, urllib.request
import fitz

DATA = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'Rainforest_860.json')))

def get(rec):
    url = DATA[rec]['doc_link']
    p = '/tmp/rf/' + hashlib.md5(url.encode()).hexdigest() + '.pdf'
    os.makedirs('/tmp/rf', exist_ok=True)
    if not os.path.exists(p):
        r = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        open(p, 'wb').write(urllib.request.urlopen(r, timeout=120).read())
    return fitz.open(p)

def show(rec, ann):
    a = DATA[rec]['annotations'][ann]; m = a['metadata']
    print('rec%d/ann%d | %s | pages %s' % (rec, ann, DATA[rec].get('company',''), m['page_numbers']))
    print('doc:', DATA[rec]['doc_link'])
    print('QUESTION:', a['question'].strip())
    print('ANSWER:', a['answer'].strip())
    print('LOGIC_ISSUE:', m.get('logic_issue', '').strip())
    print('SOLUTION (%d steps):' % len(a['solution']))
    for i, s in enumerate(a['solution']):
        print('  [%d] %s' % (i, s.strip()))

def find(rec, needles):
    doc = get(rec); n = doc.page_count
    print('%d pages' % n)
    for nd in needles:
        hits = [i for i in range(n) if nd in doc[i].get_text()]
        print('  %r -> physical pages %s' % (nd, hits[:8]))
    doc.close()

def page(rec, ph):
    doc = get(rec); print(doc[ph].get_text()); doc.close()

def around(rec, ph, needle, b=200, a=200):
    doc = get(rec); t = doc[ph].get_text(); i = t.find(needle)
    print(t[max(0,i-b):i+len(needle)+a] if i>=0 else '[%r not found on physical page %d]' % (needle, ph))
    doc.close()

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'show': show(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == 'find': find(int(sys.argv[2]), sys.argv[3:])
    elif cmd == 'page': page(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == 'around':
        rec=int(sys.argv[2]); ph=int(sys.argv[3]); needle=sys.argv[4]
        b=int(sys.argv[5]) if len(sys.argv)>5 else 200; a=int(sys.argv[6]) if len(sys.argv)>6 else 200
        around(rec, ph, needle, b, a)
