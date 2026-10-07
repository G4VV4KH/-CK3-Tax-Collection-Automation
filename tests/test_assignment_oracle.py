"""Hand-computed independent arithmetic cases; not native-game acceptance."""
import unittest
from assignment_oracle import audit


class OracleTests(unittest.TestCase):
    def matrix(self, weights, current, capacities=None):
        slots = [str(n) for n in range(len(weights[0]))]
        return {"slots": dict(zip(slots, capacities or [1] * len(slots))), "taxpayers": {
            str(i): {"slot": None if current[i] is None else str(current[i]), "gold": {slot: value for slot, value in zip(slots, row) if value is not None}}
            for i, row in enumerate(weights)}}

    def test_profitable_full_swap_uses_combined_gain(self):
        report = audit(self.matrix([[3, 9], [8, 4]], [0, 1]))
        self.assertEqual(report["profitable_pair_swaps"], [{"first": "0", "second": "1", "gain": "10"}])
        self.assertFalse(report["profitable_direct_moves"])

    def test_individual_gain_cannot_hide_larger_counterpart_loss(self):
        report = audit(self.matrix([[5, 8], [1, 7]], [0, 1]))
        self.assertEqual(report["status"], "NO_DIRECT_OR_PAIR_IMPROVEMENT")

    def test_both_cross_assignments_must_be_legal(self):
        report = audit(self.matrix([[1, 9], [None, 1]], [0, 1]))
        self.assertFalse(report["profitable_pair_swaps"])

    def test_vacancy_and_decimal_precision(self):
        report = audit(self.matrix([["1.001", "1.002"]], [0], [1, 1]))
        self.assertEqual(report["profitable_direct_moves"][0]["gain"], "0.001")

    def test_capacity_is_not_silently_ignored(self):
        report = audit(self.matrix([[1, 1], [1, 1]], [0, 0]))
        self.assertEqual(report["status"], "INVALID_ASSIGNMENT_OR_MATRIX")

    def test_three_cycle_is_explicitly_not_global_optimum_proof(self):
        report = audit(self.matrix([[10, 15, 0], [0, 10, 15], [15, 0, 10]], [0, 1, 2]))
        self.assertEqual(report["status"], "NO_DIRECT_OR_PAIR_IMPROVEMENT")
        self.assertEqual(report["native_recorded_total_gold"], "30")
        self.assertFalse(report["global_optimum_verified"])
        self.assertEqual(15 + 15 + 15, 45)


if __name__ == "__main__":
    unittest.main()
