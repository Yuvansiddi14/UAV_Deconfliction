import unittest
from src.deconfliction import calculate_distance, time_overlap, check_deconfliction

class TestDeconfliction(unittest.TestCase):
    def test_calculate_distance_2d(self):
        p1 = {"x": 0, "y": 0}
        p2 = {"x": 3, "y": 4}
        self.assertEqual(calculate_distance(p1, p2), 5)

    def test_time_overlap(self):
        self.assertTrue(time_overlap(0, 10, 5))
        self.assertFalse(time_overlap(0, 10, 15))
        
    def test_check_deconfliction_clear(self):
        primary = {
            "waypoints": [
                {"x": 0, "y": 0, "time": 0},
                {"x": 10, "y": 10, "time": 5}
            ],
            "mission_window": {"start": 0, "end": 5}
        }
        simulated = [{
            "id": "drone_test",
            "waypoints": [
                {"x": 20, "y": 20, "time": 2}
            ]
        }]
        result = check_deconfliction(primary, simulated, safety_buffer=3)
        self.assertEqual(result["status"], "clear")

if __name__ == '__main__':
    unittest.main()

