"""Freeze public source files for the proposal feasibility audit; no model fitting."""
from pathlib import Path
import urllib.request
import hashlib
import datetime
import json
import concurrent.futures

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
RAW.mkdir(parents=True, exist_ok=True)
(ROOT / 'audit').mkdir(exist_ok=True)

def download(year):
    filename = f'chaincc-teams-{year}.csv.gz'
    path = RAW / filename
    url = 'https://chaincc.lol/data/' + filename
    if not path.exists():
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=45) as response:
            raw = response.read()
        if raw[:2] != b'\x1f\x8b':
            raise ValueError('Expected a gzip file')
        path.write_bytes(raw)
    raw = path.read_bytes()
    return {'year_label': year, 'url': url, 'file': str(path.relative_to(ROOT)),
            'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    files = list(pool.map(download, [2024, 2025, 2026]))
manifest = {'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'source': 'https://chaincc.lol/free/data',
            'methodology': 'https://chaincc.lol/about/methodology', 'files': files}
(ROOT / 'audit' / 'source_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest))
