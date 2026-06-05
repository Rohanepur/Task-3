#!/usr/bin/env python3
"""GPTZero scoring helper for humanization agents.
Usage:
  python3 agent_tools/gz.py score - < file.txt      # score stdin
  python3 agent_tools/gz.py score "text..."         # score an arg
  python3 agent_tools/gz.py entry <rec> <ann>       # score the CURRENT solution text of an entry from the remediated file
Pass criterion: predicted_class == 'human'  (ai probability well below threshold).
Returns JSON: {prob, predicted_class, class_probabilities, PASS}
"""
import json, sys, urllib.request, urllib.error, time, os
KEY = open('/tmp/gptzero_key.txt').read().strip()
API = 'https://api.gptzero.me/v2/predict/text'

def score(text):
    body = json.dumps({'document': text}).encode()
    req = urllib.request.Request(API, data=body, headers={
        'x-api-key': KEY, 'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    last = None
    for attempt in range(5):
        try:
            r = json.load(urllib.request.urlopen(req, timeout=120))
            d = r['documents'][0]
            prob = d.get('completely_generated_prob')
            cls = d.get('predicted_class')
            cp = d.get('class_probabilities')
            # robust ai-probability extraction
            ai_p = None
            if isinstance(cp, dict):
                ai_p = cp.get('ai')
            return {'prob': prob, 'ai_prob': ai_p, 'predicted_class': cls,
                    'class_probabilities': cp, 'PASS': cls == 'human'}
        except urllib.error.HTTPError as e:
            last = '%d %s' % (e.code, e.read()[:200])
            if e.code in (429, 500, 502, 503): time.sleep(2 ** attempt); continue
            return {'error': last}
        except Exception as e:
            last = repr(e); time.sleep(2 ** attempt)
    return {'error': last}

def solution_text(rec, ann, path='Rainforest_860_remediated.json'):
    # Score the solution exactly as the dataset stores it: the steps joined by newlines.
    data = json.load(open(os.path.join(os.path.dirname(__file__), '..', path)))
    return '\n'.join(data[rec]['annotations'][ann]['solution'])

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'score':
        text = sys.stdin.read() if sys.argv[2] == '-' else sys.argv[2]
        print(json.dumps(score(text), indent=2))
    elif cmd == 'entry':
        print(json.dumps(score(solution_text(int(sys.argv[2]), int(sys.argv[3]))), indent=2))
