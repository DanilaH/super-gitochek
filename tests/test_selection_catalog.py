import json,unittest,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
class SelectionCatalogTests(unittest.TestCase):
 def test_coverage_and_evidence(self):
  db=json.loads((ROOT/'data/selection-catalog.json').read_text()); rows=db['projects']
  self.assertEqual(len(rows),len({r['repo'].lower() for r in rows}))
  self.assertEqual(len(rows),sum(db['counts'].values()))
  reg=json.loads((ROOT/'data/discovery-registry.json').read_text())
  for group in ('seen','pending','irrelevant'):
   self.assertEqual(sum(r['registry_group']==group for r in rows),len(reg[group]))
  for r in rows:
   self.assertTrue(r['reason']);self.assertIn(r['decision'],db['labels'])
   if r['decision']=='shortlist':
    self.assertIn(r['evidence_level'],('source_prior','source_current'));self.assertTrue(r['sources'] or r.get('source_checks'))
    self.assertNotEqual(r['core_loop'],'Не установлен сквозным чтением')
   for s in r['sources']:
    p=ROOT/s['document'];self.assertTrue(p.exists());self.assertLessEqual(s['line'],len(p.read_text().splitlines()))
   if r['evidence_level']=='source_current':
    self.assertTrue(r['source_checks']);self.assertTrue(all(s['tree_sha_matches'] for s in r['source_checks']))
if __name__=='__main__':unittest.main()
