"""Fetch public match pages and compare only the fixed 11-game training sample.
No model, EDA, validation score, or test score is computed.
Python is used for HTTP/HTML handling; the research analysis remains in R.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from datetime import datetime, timezone
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit/source_check_2026-10-20'
SAMPLE = json.loads((OUT / 'selected_training_games.json').read_text(encoding='utf-8'))
manifest = []

def fetch(url, filename):
    path = OUT / filename
    if not path.exists():
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30) as response:
            payload = response.read()
        path.write_bytes(payload)
    payload = path.read_bytes()
    manifest.append({'url': url, 'file': filename, 'sha256': hashlib.sha256(payload).hexdigest(),
                     'bytes': len(payload), 'checked_utc': datetime.now(timezone.utc).isoformat()})
    (OUT / 'source_page_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return payload.decode('utf-8-sig')

def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()

def rows(s):
    return [(r, [clean(c) for c in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', r, re.S|re.I)])
            for r in re.findall(r'<tr\b[^>]*>(.*?)</tr>', s, re.S|re.I)]

# Context-specific label correspondences, reported explicitly rather than editing raw data.
aliases = {'DN SOOPers':'Kwangdong Freecs', 'HANJIN BRION':'OK BRION',
           'Dplus Kia':'Dplus KIA', 'Gen.G':'Gen.G eSports',
           'Hanwha Life Esports':'Hanwha Life eSports'}
canon = lambda s: aliases.get(s, s).casefold()
listrows = []
for event in ['LCK Spring 2024', 'LCK Spring Playoffs 2024', 'LCK Summer 2024']:
    url = 'https://gol.gg/tournament/tournament-matchlist/' + quote(event) + '/'
    body = fetch(url, event.replace(' ', '_') + '.html')
    listrows.extend(rows(body))

results = []
for sample in SAMPLE:
    date = sample['date'][:10]
    candidates = [(raw, cells) for raw, cells in listrows if len(cells)==7
                  and cells[-1]==date
                  and {canon(cells[1]),canon(cells[3])} ==
                      {canon(sample['team_name']),canon(sample['red_team_name'])}]
    assert len(candidates)==1, (sample['game_id'], 'series matching', len(candidates))
    raw, cells = candidates[0]
    first = re.search(r'game/stats/(\d+)/page-summary/', raw).group(1)
    summary_url = f'https://gol.gg/game/stats/{first}/page-summary/'
    summary = fetch(summary_url, f'gol_{first}_summary.html')
    games = list(dict.fromkeys(re.findall(r'game/stats/(\d+)/page-game/', summary)))
    game = games[sample['game_number']-1]
    game_url = f'https://gol.gg/game/stats/{game}/page-game/'
    full_url = f'https://gol.gg/game/stats/{game}/page-fullstats/'
    page = fetch(game_url, f'gol_{game}_game.html')
    full = fetch(full_url, f'gol_{game}_fullstats.html')
    teamheaders = {}
    for side in ['blue','red']:
        match = re.search(r'<div[^>]+class="[^"]*'+side+r'-line-header[^\"]*"[^>]*>(.*?)</div>',page,re.S)
        text = clean(match.group(1))
        name, outcome = text.rsplit(' - ',1)
        teamheaders[side] = {'name':name,'outcome':outcome.strip()}
    date_observed = re.search(r'(2024-\d{2}-\d{2})\s*\(', clean(page)).group(1)
    patch_observed = re.search(r'\bv(14\.\d+)\b', clean(page)).group(1)
    duration_match = re.search(r'Game Time\s+(\d+):(\d+)',clean(page))
    duration = int(duration_match.group(1))*60+int(duration_match.group(2))
    fullrows = dict((c[0],c[1:]) for _,c in rows(full) if len(c)==11)
    early = {}
    for label, field in [('GD@15','golddiffat15'),('CSD@15','csdiffat15'),('XPD@15','xpdiffat15')]:
        vals = [int(x) for x in fullrows[label]]
        assert sum(vals[:5]) == -sum(vals[5:]), (game, label)
        early[field] = {'local':sample[field], 'external':sum(vals[:5]),
                        'match':sample[field]==sum(vals[:5]), 'blue_player_values':vals[:5],
                        'red_player_values':vals[5:]}
    chart = re.search(r'var golddatas\s*=\s*(.*?);',page,re.S).group(1)
    labels = re.findall(r"'([^']+)'", re.search(r'labels:\s*\[(.*?)\]',chart,re.S).group(1))
    golds = [float(x) for x in re.search(r"label:\s*'Gold'.*?data:\s*\[(.*?)\]",chart,re.S).group(1).split(',') if x.strip()]
    assert len(labels)==len(golds)
    gold_chart15 = golds[labels.index('15')]
    # Normalize patch padding componentwise, never with a decimal conversion.
    patch_key = lambda x: tuple(int(p) for p in x.split('.'))
    result = {'game_id':sample['game_id'], 'game_number':sample['game_number'],
              'local_date':date, 'external_date':date_observed, 'date_match':date==date_observed,
              'local_patch':sample['patch'], 'external_patch':patch_observed,
              'patch_match':patch_key(sample['patch'])==patch_key(patch_observed),
              'local_blue':sample['team_name'], 'external_blue':teamheaders['blue']['name'],
              'local_red':sample['red_team_name'], 'external_red':teamheaders['red']['name'],
              'team_side_match_with_documented_aliases':
                  canon(sample['team_name'])==canon(teamheaders['blue']['name']) and
                  canon(sample['red_team_name'])==canon(teamheaders['red']['name']),
              'literal_team_name_match':sample['team_name']==teamheaders['blue']['name'] and
                  sample['red_team_name']==teamheaders['red']['name'],
              'local_blue_win':sample['result'], 'external_blue_win':teamheaders['blue']['outcome']=='WIN',
              'result_match':sample['result']==(teamheaders['blue']['outcome']=='WIN'),
              'external_complementary_outcomes':{teamheaders['blue']['outcome'],teamheaders['red']['outcome']}=={'WIN','LOSS'},
              'local_duration_seconds':sample['gamelength'], 'external_duration_seconds':duration,
              'duration_difference_seconds':sample['gamelength']-duration,
              'early_fields':early,'gold_chart15':gold_chart15,
              'gold_chart15_match':gold_chart15==sample['golddiffat15'],
              'kills15_status':'not_yet_checked','source_urls':[game_url,full_url],
              'selection_reason':sample['selection_reason']}
    results.append(result)
    (OUT / 'crosscheck_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(sample['game_id'], game, 'date',result['date_match'],'patch',result['patch_match'],
          'outcome',result['result_match'],'early',[x['match'] for x in early.values()],
          'duration_delta',result['duration_difference_seconds'],flush=True)
assert len(results)==11
print('Finished fixed sample. Raw research files were not modified.',flush=True)
