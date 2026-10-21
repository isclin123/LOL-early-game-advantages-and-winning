"""Check 15-minute kill differences in the already selected source-check sample."""
from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import html
import json
import re

OUT = Path(__file__).resolve().parents[1] / 'audit/source_check_2026-10-20'
samples = {r['game_id']:r for r in json.loads((OUT/'selected_training_games.json').read_text())}
results = json.loads((OUT/'crosscheck_results.json').read_text())
assert len(results)==11
clean = lambda s: re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip()

def check(record):
    game = re.search(r'/stats/(\d+)/',record['source_urls'][0]).group(1)
    url = f'https://gol.gg/game/stats/{game}/page-timeline/'
    path = OUT / f'gol_{game}_timeline.html'
    if not path.exists():
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response:
            payload = response.read()
        path.write_bytes(payload)
    payload = path.read_bytes()
    events = []
    for raw in re.findall(r'<tr\b[^>]*>(.*?)</tr>',payload.decode('utf-8-sig'),re.S):
        if '/kill-icon.png' not in raw:
            continue
        cells = re.findall(r'<td\b[^>]*>(.*?)</td>',raw,re.S)
        timestamp = clean(cells[0])
        m,s = [int(x) for x in timestamp.split(':')]
        side = re.search(r'/(blue|red)side-icon\.png',cells[1]).group(1)
        events.append({'time':timestamp,'seconds':60*m+s,'side':side,
                       'killer':clean(cells[2]),'target':clean(cells[-1])})
    full = (OUT/f'gol_{game}_fullstats.html').read_text(encoding='utf-8-sig')
    total_kills = None
    for raw in re.findall(r'<tr\b[^>]*>(.*?)</tr>',full,re.S):
        cells = [clean(x) for x in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',raw,re.S)]
        if len(cells)==11 and cells[0]=='Kills':
            values = [int(x) for x in cells[1:]]
            total_kills = {'blue':sum(values[:5]),'red':sum(values[5:])}
    assert total_kills is not None
    parsed_totals = {s:sum(e['side']==s for e in events) for s in ['blue','red']}
    early = {s:sum(e['side']==s and e['seconds']<=900 for e in events) for s in ['blue','red']}
    local = samples[record['game_id']]['killdiffat15']
    data = {'game_id':record['game_id'],'url':url,'local_difference':local,
            'early_kills':early,'external_difference':early['blue']-early['red'],
            'difference_match':early['blue']-early['red']==local,
            'events_at_15_00':sum(e['seconds']==900 for e in events),
            'full_game_kills_from_table':total_kills,'full_game_kills_from_timeline':parsed_totals,
            'full_game_total_check':total_kills==parsed_totals,
            'early_kill_events':[e for e in events if e['seconds']<=900]}
    source = {'url':url,'file':path.name,'sha256':hashlib.sha256(payload).hexdigest(),
              'bytes':len(payload),'checked_utc':datetime.now(timezone.utc).isoformat()}
    print(record['game_id'],'kill difference',local,data['external_difference'],
          'total_check',data['full_game_total_check'],flush=True)
    return data,source

with ThreadPoolExecutor(max_workers=3) as pool:
    checked = list(pool.map(check,results))
(OUT/'kill_timeline_results.json').write_text(json.dumps([x[0] for x in checked],indent=2),encoding='utf-8')
(OUT/'timeline_page_manifest.json').write_text(json.dumps([x[1] for x in checked],indent=2),encoding='utf-8')
print('Finished timeline checks for all 11 training games.',flush=True)
