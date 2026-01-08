import unittest
from models import Subscription
from datetime import datetime

class TestOperation(unittest.TestCase):

    def test_to_dict(self):
        op = Subscription(100, "Food", "2025-12-27", "Test comment", "expense")
        d = op.to_dict()
        self.assertEqual(d["amount"], 100)
        self.assertEqual(d["category"], "Food")
        self.assertEqual(d["date"], "2025-12-27")
        self.assertEqual(d["comment"], "Test comment")
        self.assertEqual(d["op_type"], "expense")

    def test_date_conversion(self):
        op = Subscription(50, "Salary", "2025-12-30", "Monthly", "income")
        self.assertIsInstance(op.date, datetime)
        self.assertEqual(op.date.strftime("%Y-%m-%d"), "2025-12-30")

if __name__ == "__main__":
    unittest.main()
