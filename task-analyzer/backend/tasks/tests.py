import unittest
from .scoring import analyze_tasks, score_task, detect_cycle

class ScoringTests(unittest.TestCase):
    def test_basic_scoring(self):
        tasks = [
            {'id':'a','title':'A','due_date':'2025-12-01','estimated_hours':2,'importance':8,'dependencies':[]},
            {'id':'b','title':'B','due_date':'2023-01-01','estimated_hours':1,'importance':5,'dependencies':[]},
        ]
        res = analyze_tasks(tasks)
        self.assertIn('tasks', res)
        self.assertTrue(len(res['tasks'])==2)

    def test_cycle_detection(self):
        tasks = [
            {'id':'a','title':'A','dependencies':['b']},
            {'id':'b','title':'B','dependencies':['a']},
        ]
        res = analyze_tasks(tasks)
        self.assertTrue(res['has_cycle'])

if __name__ == '__main__':
    unittest.main()
