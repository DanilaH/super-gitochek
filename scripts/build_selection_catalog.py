"""Build an honest selection view without changing discovery-registry semantics."""
import json,re,collections,pathlib,html
ROOT=pathlib.Path(__file__).resolve().parents[1]
DOCS=sorted((ROOT/'docs').glob('*.md'))
DOCS=[p for p in DOCS if p.name not in {'CATALOG_REVIEW_2026-10-14.md','DECISIONS.md','CATALOG_SOURCE_CHECKS_2026-10-14.md'}]
LABELS={'shortlist':'Выбирать в первую очередь','mechanic':'Отдельная механика','reserve':'Игровой резерв','complex':'Слишком большой объём','tool':'Инструмент / библиотека','learning':'Учебный пример / шаблон','noise':'Не игровая находка','incomplete':'Неполная реализация','uncertain':'Недостаточно данных','duplicate':'Копия / зеркало'}
reg=json.loads((ROOT/'data/discovery-registry.json').read_text())
rows={}
for group in ['seen','pending','irrelevant']:
 values=reg[group].items() if isinstance(reg[group],dict) else [(None,v) for v in reg[group]]
 for registry_id,v in values:
  x=v.get('item',{}) if group=='seen' else v.get('repo',{}) if group=='irrelevant' else v
  repo=x.get('full_name')
  if not repo: raise ValueError((group,v))
  rows[repo.lower()]={'repo':repo,'id':x.get('id') or registry_id,'description':x.get('description') or '', 'registry_group':group,'language':x.get('language') or '', 'stack_hint':x.get('engine') or x.get('discovery_track') or '', 'sources':[]}
ignore={'docs','data','scripts','tests','js','game','src','assets','ui_left','hold','owner'}
for p in DOCS:
 text=p.read_text(); lines=text.splitlines(); heading=''
 for i,line in enumerate(lines):
  if line.startswith('#'):heading=line.lstrip('# ')
  names=re.findall(r'https://github\.com/([\w.-]+/[\w.-]+)',line)+re.findall(r'`([\w.-]+/[\w.-]+)`',line)
  for repo in set(names):
   repo=repo.removesuffix('.git').rstrip('.')
   owner,name=repo.split('/')
   if owner.lower() in ignore|{'danilah','topics','features','sponsors','search','orgs'} or name.lower().endswith(('.md','.js','.ts','.json')):continue
   k=repo.lower()
   if k not in rows:rows[k]={'repo':repo,'id':None,'description':'','registry_group':'manual_only','language':'','stack_hint':'','sources':[]}
   excerpt=line if not line.startswith('#') else ' '.join(lines[i+1:i+8])
   source={'document':'docs/'+p.name,'line':i+1,'heading':heading,'excerpt':excerpt[:1000]}
   if not any(s['document']==source['document'] and s['line']==source['line'] for s in rows[k]['sources']):rows[k]['sources'].append(source)
readmes={x['repo'].lower():x for x in json.loads((ROOT/'data/review-evidence.json').read_text())}
overrides=json.loads((ROOT/'data/review-decisions.json').read_text())

def match(pattern,t):return re.search(pattern,t,re.I)

def classify(r):
 k=r['repo'].lower(); d=r['description']; rd=readmes.get(k,{}); text=d+' '+rd.get('excerpt',''); n=k.split('/')[1]; t=n+' '+text
 r.update(decision='uncertain',reason='Описания недостаточно для содержательного отбора; в витрину выбора не включён.',evidence_level='metadata',review_method='metadata_rule',core_loop='',production_burden='Не оценён',next_check='Прочитать игровой цикл перед повышением приоритета.',playtest='Нет подтверждённого playtest',mobile='Не проверено',license_status='Не проверено',related_to='')
 if rd.get('excerpt'):r['evidence_level']='readme';r['readme_evidence']=rd
 elif rd:r['readme_evidence']=rd
 if match(r'awesome|list of|curated list|roadmap|collection of.*(resources|tutorial)|datasets|papers|interview|cheatsheet',t):
  r.update(decision='learning',reason='Подборка материалов, данных или учебных ресурсов; не отдельная игра.')
 elif match(r'copilot|llm|latex|mechaduino|test data|data factory|tla\+|devops|text mining|machine learning|nocom-explanation|pixel-agents|token claim|airdrop',t):
  r.update(decision='noise',reason='По описанию это ПО/материалы вне задачи поиска самостоятельной игровой механики.')
 elif match(r'plugin|\bsdk\b|\blibrary\b|\blibraries\b|framework|toolkit|wrapper|extension|editor|shader|bindings|gamepadtest|virtualgamepad|nineslice|imehelper|spriteforge|gamemode api|game ui|gui and|voip|开发框架|游戏框架|游戏算法|rendering engine|physics engine|game engine (written|for|built)|implementation of.*xna',t):
  r.update(decision='tool',reason='Описан инструмент разработки, библиотека, SDK или техническая подсистема; не самостоятельный игровой цикл.')
 elif match(r'tutorial|starter|boilerplate|template|scaffold|course|lesson|exercise|learning project|educational|first.*game|учеб|教程|课程|lab\b',t):
  r.update(decision='learning',reason='Учебный проект или шаблон; наличие примера не подтверждает готовую игру с прогрессией.')
 elif match(r'mmorpg|multiplayer|multi-player|networked|metroidvania|roguelike|roguelite|\brpg\b|role.playing|vampire survivors|deck.build|open.world|blockchain|web3|solana|3d.*(shooter|battle)|village.build|management game|platformer|tower.defen|side.scroll',t):
  r.update(decision='complex',reason='Заявленный жанр/состав систем выше текущего минимального масштаба; оценка по описанию, отдельная механика не исключена.',production_burden='Высокий для целой игры')
 elif match(r'game|puzzle|clicker|incremental|arcade|flappy|tetris|snake|pong|chess|2048|minesweeper|游戏|遊戲|игра',t):
  r.update(decision='reserve',reason='Игра или игровой прототип по описанию. Отличительная петля и пригодность для нашего масштаба не подтверждены.',next_check='Нужны код ввода, награды и развития; пока ниже проверенных кандидатов.')
 if r['sources']:
  r.update(evidence_level='prior_report',review_method='prior_report',decision='reserve',reason='Есть ручной разбор в архиве. Подробности и ограничения — в связанных фрагментах; в основной выбор автоматически не повышен.')
  # Most recent explicit table verdict overrides a generic metadata guess.
  verdicts=[s for s in r['sources'] if s['excerpt'].startswith('|') and (' | ' in s['excerpt'])]
  if verdicts:
   s=sorted(verdicts,key=lambda s:s['document'])[-1];v=s['excerpt'].split(' | ',1)[-1].strip(' |');r['reason']=v[:700]
   if match(r'только дерево|код не (провер|проч|разбир)|готовность не установлена|не удалось|в очередь|остаётся в очереди|не приравнивать',v):r['decision']='uncertain'
   elif match(r'пустая заготовка|реализации не обнаружено|пустой README|не реализован|закомментирован',v):r['decision']='incomplete'
   elif match(r'редактор|помощник для WoW|не самостоятельная игра|инструмент, не игра',v):r['decision']='tool'
   elif match(r'дорог|выше минимального|не минимальный|крупн|не тактильный минимализм',v):r['decision']='complex';r['production_burden']='Высокий для целой игры'
  r['next_check']='Свериться с ограничениями архивного разбора перед прототипированием.'
 if k in overrides:r.update(overrides[k]);r['review_method']='editorial'
 if not r['core_loop']:r['core_loop']='Не установлен сквозным чтением'
 r['decision_label']=LABELS[r['decision']]
 r['url']='https://github.com/'+r['repo']
 return r
items=[classify(r) for r in rows.values()]
order=list(LABELS)
items.sort(key=lambda r:(order.index(r['decision']),r.get('rank',999),r['repo'].lower()))
counts=dict(collections.Counter(r['decision'] for r in items)); ev=dict(collections.Counter(r['evidence_level'] for r in items))
external={}
for p in DOCS:
 for url in set(re.findall(r'https://[a-zA-Z0-9-]+\.itch\.io/[a-zA-Z0-9_-]+',p.read_text())):
  external.setdefault(url,[]).append('docs/'+p.name)
result={'external_references':[{'url':u,'sources':s,'status':'Авторская веб-страница из архива; не отдельный подтверждённый репозиторий'} for u,s in sorted(external.items())],'schema_version':1,'review_date':'2026-10-14','scope':'Реестр + 18 ручных документов; не число независимых идей или готовых игр','counts':counts,'evidence_counts':ev,'total':len(items),'labels':LABELS,'projects':items}
(ROOT/'data/selection-catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'total':len(items),'groups':dict(collections.Counter(r['registry_group'] for r in items)),'counts':counts,'evidence':ev},ensure_ascii=False,indent=2))
template=(ROOT/'catalog/template.html').read_text()
(ROOT/'catalog/index.html').write_text(template.replace('__DATA__',json.dumps(result,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')))
