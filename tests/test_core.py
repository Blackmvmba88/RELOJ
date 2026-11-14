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

    def test_rejects_out_of_range_bezel(self):
        issues = validate_watch(WatchSpec(bezel_width_mm=21.0))
        self.assertTrue(any(issue.code == "RANGE" and issue.field == "bezel_width_mm"
                            for issue in issues))

    def test_malformed_numeric_type_does_not_crash_validation(self):
        issues = validate_watch(WatchSpec(case_diameter_mm="large"))
        self.assertTrue(any(issue.code == "TYPE" and issue.field == "case_diameter_mm"
                            for issue in issues))

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
