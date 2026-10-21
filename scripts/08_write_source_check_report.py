"""Write a source-check report from saved observations, without fitting models."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'audit/source_check_2026-10-20'
rows = json.loads((OUT/'crosscheck_results.json').read_text())
kills = {r['game_id']:r for r in json.loads((OUT/'kill_timeline_results.json').read_text())}
assert len(rows)==len(kills)==11
fields = ['golddiffat15','killdiffat15','xpdiffat15','csdiffat15']
labels = ['经济差','击杀差','经验差','补刀差']
for row in rows:
    k = kills[row['game_id']]
    row['kills15_status'] = 'cross_checked' if k['difference_match'] and k['full_game_total_check'] and not k['events_at_15_00'] else 'needs_review'
    row['early_fields']['killdiffat15'] = {'local':k['local_difference'], 'external':k['external_difference'],
                                          'match':k['difference_match']}
    row['source_urls'].append(k['url'])
(OUT/'combined_results.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
counts = {f:sum(r['early_fields'][f]['match'] for r in rows) for f in fields}
checks = {'比赛日期':sum(r['date_match'] for r in rows),
          '蓝红双方（明确记录名称对应后）':sum(r['team_side_match_with_documented_aliases'] for r in rows),
          '蓝方最终胜负':sum(r['result_match'] and r['external_complementary_outcomes'] for r in rows),
          '版本主次编号（保留字符串）':sum(r['patch_match'] for r in rows),
          '比赛时长（秒）':sum(r['duration_difference_seconds']==0 for r in rows)}
all_numeric = all(v==11 for v in counts.values()) and all(v==11 for v in checks.values())
kill_parser_ok = all(k['full_game_total_check'] and k['events_at_15_00']==0 for k in kills.values())
assert all_numeric and kill_parser_ok and all(r['gold_chart15_match'] for r in rows), 'Review discrepancies before publishing a passed conclusion.'
lines = ['# LOL 数据来源抽查记录', '', '核查日期：2026 年 10 月 20 日。', '',
'## 结论', '',
'**本次选取的 11 场训练比赛，最终胜负、比赛日期、版本编号、比赛时长及四项 15 分钟指标均与外部统计页一致。** 本轮未发现这 11 场的核心数值错误，现有数据可以继续用于后续分析。', '',
'发现的主要问题是队伍名称的历史显示：本地部分 2024 年记录使用 DN SOOPers 或 HANJIN BRION，比赛当时的统计页分别写 Kwangdong Freecs 或 OK BRION。以下按具体比赛记录对应，不修改原始文件，也不据此自动合并全部历史队伍。', '',
'这是有目的的跨网站抽样核对，不是全部 1,637 场数据的认证，也不是对视频或 Riot 原始事件数据的独立重建。两个网站可能共享上游记录；数值一致并不能排除共同来源的错误。', '',
'## 抽样规则与范围', '',
'仅从固定的 313 场初始训练数据中选择：每个版本按日期和比赛 ID 排序后的第一场（8 场），经济差最小和最大的两场，以及最早出现补刀差或经验差为零的一场。去重后共 11 场，覆盖全部 8 个训练版本。没有按胜负挑选样本。', '',
'这不是随机样本，因此不能用通过比例估计总体错误率。没有检查验证或测试样本的预测关系，没有创建探索性分析报告，没有拟合模型。用于检索的赛事列表可能显示其他比赛，但比较结果只提取上述固定 11 场。', '',
'抽样文件：[比赛清单](audit/source_check_2026-10-20/selected_training_games.json)；抽样代码：[R 脚本](scripts/05_select_source_check.R)。', '',
'## 外部来源及核对方法', '',
'主要对照来源是 Games of Legends（第三方比赛统计网站）：通过赛事、日期、双方名称和局号定位比赛，再核对蓝红方、结果、时长和版本。具体比赛页链接列在下表，页面快照及 SHA-256 均已保存。', '',
'- 经济差、经验差和补刀差：分别将蓝方五名选手的 `GD@15`、`XPD@15`、`CSD@15` 相加，与本地蓝减红队伍差值比较；同时确认红方五人的合计为相反数。',
'- 经济差另与比赛页经济时间线中明确标为第 15 分钟的点进行核对。这是同一网站内的额外检查，不算新增独立来源。',
'- 击杀差：从事件时间线累计截至 15:00 的蓝、红双方击杀事件，再相减。11 场均没有显示恰好发生在 15:00 的击杀，避免了该秒边界的归属歧义。',
'- 为检查事件解析是否遗漏，每场整场的蓝红击杀事件总数还与赛后击杀表核对，11 场均一致。赛后数据只用于来源核查，不进入预测指标。',
'- `14.01` 与 `14.1` 按主、次版本组成部分视为同一编号，不把版本当小数转换；本次没有验证更细的热修复版本标识。', '',
'## 逐项结果', '', '| 核查字段 | 一致场数 | 说明 |', '|---|---:|---|']
for name,n in checks.items():
    lines.append(f'| {name} | {n}/11 | 对照具体比赛页 |')
for f,label in zip(fields,labels):
    lines.append(f'| 15 分钟{label} | {counts[f]}/11 | 精确数值一致 |')
lines += ['', '下表每个数值均为“本地值＝外部值”；正数表示蓝方领先。', '',
'| 日期 | 外部名称：蓝方 — 红方 | 局号 | 版本（本地） | 经济差 | 击杀差 | 经验差 | 补刀差 | 证据 |',
'|---|---|---:|---|---:|---:|---:|---:|---|']
for r in rows:
    nums = [str(r['early_fields'][f]['local']) for f in fields]
    links = f"[比赛]({r['source_urls'][0]}) / [指标]({r['source_urls'][1]}) / [事件]({r['source_urls'][2]})"
    lines.append('| '+' | '.join([r['local_date'],r['external_blue']+' — '+r['external_red'],
                 str(r['game_number']),r['local_patch']]+nums+[links])+' |')
zero = [r for r in rows if r['early_fields']['csdiffat15']['local']==0]
lines += ['', '**零值核对：** '+', '.join(r['game_id'] for r in zero)+
' 的补刀差为 0，外部五名蓝方选手的 CSD@15 合计也为 0。因此这个具体零值有外部支持，不能因为为零就当作缺失；它并不证明其他所有零值都有效。', '',
'## 名称差异与处理建议', '',
'| 本地名称 | 对应比赛页名称 | 性质与处理 |', '|---|---|---|']
aliases = sorted({(r['local_'+s],r['external_'+s]) for r in rows for s in ['blue','red'] if r['local_'+s]!=r['external_'+s]})
for a,b in aliases:
    note = '历史显示名称差异；仅对本次匹配比赛记录对应' if a in ['DN SOOPers','HANJIN BRION'] else '大小写或名称写法不同'
    lines.append(f'| {a} | {b} | {note} |')
lines += ['',
'后续展示历史比赛时，应使用当时的名称或同时注明原始名称。连接原始记录继续使用比赛 ID、蓝红方和队伍 ID；本次没有验证所有队伍 ID 跨年份是否始终代表同一实体。四项前期数值和胜负不受本次发现的名称显示问题影响。', '',
'## 已确认与仍未确认的边界', '',
'已确认：所抽 11 场比赛的对阵方向、最终结果、日历日期、版本主次编号、时长，以及本研究使用的四项 15 分钟差值。', '',
'尚未确认：精确开赛时间和原始时间字段的时区、所有比赛的完整覆盖、全部队伍的历史身份映射、其他年份及赛区的逐条正确性、早期统计的底层计算机制，以及两个网站是否共享同一上游采集误差。经济总量和其他非核心字段未在本轮逐项外部核对。', '',
'[ChainCC 数据页](https://chaincc.lol/free/data)说明有 10 和 15 分钟差值；其[方法说明](https://chaincc.lol/about/methodology)列出 Oracle’s Elixir 等来源。此次核对使用 Games of Legends，不把 Oracle’s Elixir 标记为已经取得的第二份数据集。', '',
'当前无需仅因来源疑虑更换整套数据。保留原始快照，下一阶段可以在上述限制下继续；若将来发现具体不一致，应先定位字段与比赛，再决定是否扩展审计。', '',
'## 复现与证据文件', '',
'- [全部比较结果](audit/source_check_2026-10-20/combined_results.json)：本地、外部数值及每项状态。',
'- [击杀事件核对](audit/source_check_2026-10-20/kill_timeline_results.json)：15 分钟前的事件和整场解析检查。',
'- [比赛统计页清单](audit/source_check_2026-10-20/source_page_manifest.json)与[事件页清单](audit/source_check_2026-10-20/timeline_page_manifest.json)：URL、本地快照和哈希。',
'- [来源页面匹配脚本](scripts/06_crosscheck_sources.py)、[击杀时间线脚本](scripts/07_check_kill_timelines.py)、[本报告生成脚本](scripts/08_write_source_check_report.py)。',
'- Python 仅用于下载和解析网页；项目统计分析仍使用 R。脚本优先读取已保存的网页快照，避免复核时静默替换来源。', '',
'本轮只做来源抽查，原始研究数据、分组和 proposal 均未改动。']
(ROOT/'07_数据来源抽查记录.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Report written; all 44 early-feature comparisons match, with explicitly recorded name differences.')
