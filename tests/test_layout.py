import unittest
from layout import generate,feasible_region
class GeometryTests(unittest.TestCase):
 def test_setback_analytic_square(self):
  terrain,region=feasible_region([(0,0),(20,0),(20,20),(0,20)],2)
  self.assertAlmostEqual(region.area,256)
 def test_all_generated_buildings_obey_constraints(self):
  result=generate([(0,0),(65,0),(65,25),(48,25),(48,52),(0,52)])
  self.assertTrue(result['layouts'])
  for row in result['layouts']:
   self.assertLessEqual(row['coverage'],.45+1e-9)
   for i,b in enumerate(row['buildings']):
    self.assertTrue(result['region'].covers(b))
    for other in row['buildings'][i+1:]:
     self.assertAlmostEqual(b.intersection(other).area,0)
     self.assertGreaterEqual(b.distance(other)+1e-9,3)
 def test_infeasible_and_invalid_inputs(self):
  square=[(0,0),(10,0),(10,10),(0,10)]
  self.assertEqual(generate(square,setback=6)['layouts'],[])
  for kwargs in [{'step':0},{'gap':-1},{'max_coverage':2},{'width':float('nan')}]:
   with self.assertRaises(ValueError):generate(square,**kwargs)
  with self.assertRaises(ValueError):feasible_region([(0,0),(10,10),(0,10),(10,0)],1)
