import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from reloj_core.models import WatchSpec
from reloj_core.luxury import COMPONENTS, FINISHES, generate_luxury_scad, export_luxury_scad


class LuxuryTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(generate_luxury_scad(WatchSpec()), generate_luxury_scad(WatchSpec()))

    def test_integrated_lugs_and_crown(self):
        model = generate_luxury_scad(WatchSpec())
        self.assertIn("module integrated_lugs()", model)
        self.assertIn("module crown()", model)
        self.assertIn("hull()", model)

    def test_selectable_components(self):
        for component in COMPONENTS:
            with self.subTest(component=component):
                self.assertIn(f'component = "{component}";',
                              generate_luxury_scad(WatchSpec(), component=component))

    def test_three_finishes(self):
        for finish in FINISHES:
            with self.subTest(finish=finish):
                self.assertIn("metal_color =", generate_luxury_scad(WatchSpec(), finish=finish))

    def test_rejects_invalid_geometry(self):
        with self.assertRaises(ValueError):
            generate_luxury_scad(WatchSpec(lug_to_lug_mm=40))

    def test_rejects_unknown_component(self):
        with self.assertRaises(ValueError):
            generate_luxury_scad(WatchSpec(), component="movement")

    def test_rejects_bad_facets(self):
        with self.assertRaises(ValueError):
            generate_luxury_scad(WatchSpec(), facets=True)

    def test_exports_file(self):
        with TemporaryDirectory() as folder:
            target = Path(folder) / "luxury.scad"
            export_luxury_scad(WatchSpec(), target)
            self.assertIn("module assembly()", target.read_text())


if __name__ == "__main__":
    unittest.main()
