import unittest

from reloj_core import WatchSpec, calculate_geometry, validate_watch


class WatchCoreTests(unittest.TestCase):
    def test_default_spec_is_valid(self):
        self.assertEqual(validate_watch(WatchSpec()), [])

    def test_geometry_is_deterministic(self):
        spec = WatchSpec()
        first = calculate_geometry(spec)
        second = calculate_geometry(spec)
        self.assertEqual(first, second)
        self.assertAlmostEqual(first.dial_opening_diameter_mm, 36.0)
        self.assertAlmostEqual(first.lug_to_lug_ratio, 1.175)

    def test_rejects_impossible_bezel(self):
        spec = WatchSpec(bezel_width_mm=21.0)
        codes = {issue.code for issue in validate_watch(spec)}
        self.assertIn("PROPORTION", codes)

    def test_diver_target_is_warning_not_certification(self):
        spec = WatchSpec(family="diver", water_resistance_m=50)
        issues = validate_watch(spec)
        self.assertTrue(any(issue.code == "DIVER_RATING" and issue.severity == "warning"
                            for issue in issues))

    def test_unknown_json_fields_are_rejected(self):
        with self.assertRaises(ValueError):
            WatchSpec.from_dict({"case_diamter_mm": 40})


if __name__ == "__main__":
    unittest.main()
