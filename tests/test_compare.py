import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('compare',Path(__file__).parents[1]/'scripts/compare.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run={'context':{k:'synthetic' for k in module.CONTEXT},'samples':[{'case':'report','duration_ms':n,'queries':10,'status':200,'result_hash':hashlib.sha256(b'fixed-result').hexdigest()} for n in [100,110,90]]}

    def compare(self, candidate):
        root=Path(self.tmp.name)
        (root/'before.json').write_text(json.dumps(self.run))
        (root/'after.json').write_text(json.dumps(candidate))
        return module.compare(root/'before.json',root/'after.json')

    def test_reports_measured_reduction(self):
        after=copy.deepcopy(self.run)
        for row in after['samples']:row['duration_ms']/=2
        self.assertEqual(self.compare(after)['comparisons'][0]['processing_reduction_percent'],50)

    def test_rejects_faster_wrong_results(self):
        after=copy.deepcopy(self.run);after['samples'][0]['result_hash']='a'*64
        with self.assertRaisesRegex(ValueError,'Authoritative'):self.compare(after)

    def test_rejects_changed_runtime(self):
        after=copy.deepcopy(self.run);after['context']['runtime']='different'
        with self.assertRaisesRegex(ValueError,'contexts'):self.compare(after)

    def test_rejects_invalid_samples(self):
        for key,value in [('status',500),('duration_ms',float('nan')),('queries',-1),('result_hash','')]:
            with self.subTest(key=key):
                after=copy.deepcopy(self.run);after['samples'][0][key]=value
                with self.assertRaises(ValueError):self.compare(after)

    def test_reports_regression(self):
        after=copy.deepcopy(self.run)
        for row in after['samples']:row['duration_ms']*=1.3
        self.assertEqual(self.compare(after)['comparisons'][0]['processing_reduction_percent'],-30)

    def test_rejects_missing_case(self):
        after=copy.deepcopy(self.run)
        for row in after['samples']:row['case']='other'
        with self.assertRaisesRegex(ValueError,'case sets'):self.compare(after)

class CommandTests(unittest.TestCase):
    setUp = ComparisonTests.setUp
    compare = ComparisonTests.compare

    def test_cli_rejects_failed_threshold(self):
        import subprocess, sys
        root=Path(self.tmp.name)
        for filename in ['before.json','after.json']:
            (root/filename).write_text(json.dumps(self.run))
        process=subprocess.run([sys.executable,str(Path(__file__).parents[1]/'scripts/compare.py'),str(root/'before.json'),str(root/'after.json'),'--min-reduction','50','--target-case','report'],capture_output=True,text=True)
        self.assertEqual(process.returncode,3)
        self.assertEqual(json.loads(process.stdout)['threshold_failures'],['report: reduction below threshold'])

    def test_rejects_malformed_objects(self):
        for invalid in [[], {'context':[], 'samples':[]}, {'context':self.run['context'],'samples':[None]}]:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError): self.compare(invalid)

if __name__ == '__main__':
    unittest.main()
