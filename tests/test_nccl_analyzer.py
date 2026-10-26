import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from nccl_analyzer import parse_output, summarize


class NCCLAnalyzerTest(unittest.TestCase):
    def test_parses_and_scores(self):
        text = (Path(__file__).parent / "fixtures" / "all_reduce.txt").read_text()
        summary = summarize(parse_output(text, 200))
        self.assertEqual(summary["samples"], 3)
        self.assertEqual(summary["status"], "healthy")
        self.assertAlmostEqual(summary["peak"]["efficiency_pct"], 87.39)

    def test_rejects_empty_data(self):
        with self.assertRaises(ValueError):
            parse_output("header only", 200)


if __name__ == "__main__":
    unittest.main()
