import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from reloj_core import WatchSpec
from reloj_core.cad import generate_scad, export_scad


class CADTests(unittest.TestCase):
    def test_deterministic(self):
        spec = WatchSpec()
        self.assertEqual(generate_scad(spec), generate_scad(spec))

    def test_parametric_dimensions(self):
        source = generate_scad(WatchSpec(case_diameter_mm=42, lug_to_lug_mm=50))
        self.assertIn("case_d = 42.0000;", source)
        self.assertIn("lug_span = 50.0000;", source)
        self.assertIn("module bezel_ring()", source)
        self.assertIn("module lugs()", source)

    def test_invalid_geometry_rejected(self):
        with self.assertRaises(ValueError):
            generate_scad(WatchSpec(case_diameter_mm=10))

    def test_invalid_facets_rejected(self):
        with self.assertRaises(ValueError):
            generate_scad(WatchSpec(), facets=12)

    def test_write_scad(self):
        with TemporaryDirectory() as temp:
            target = Path(temp) / "watch.scad"
            export_scad(WatchSpec(), target)
            self.assertIn("watch_concept();", target.read_text())


if __name__ == "__main__":
    unittest.main()
