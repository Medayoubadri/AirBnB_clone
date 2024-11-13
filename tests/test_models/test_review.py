#!/usr/bin/python3

"""
Unit tests for the Review class.
"""

import unittest
from models.review import Review
from models.base_model import BaseModel

class TestReview(unittest.TestCase):
    """Tests for the Review class."""

    def setUp(self):
        """Sets up a Review instance before each test."""
        self.review = Review()
        self.review.place_id = "1234"
        self.review.user_id = "5678"
        self.review.text = "Great place to stay!"

    def test_inheritance(self):
        """Test that Review class inherits from BaseModel."""
        self.assertIsInstance(self.review, BaseModel)

    def test_attributes(self):
        """Test that Review has the correct attributes."""
        self.assertEqual(self.review.place_id, "1234")
        self.assertEqual(self.review.user_id, "5678")
        self.assertEqual(self.review.text, "Great place to stay!")

    def test_str_method(self):
        """Test the __str__ method for correct output format."""
        expected_output = f"[Review] ({self.review.id}) {self.review.__dict__}"
        self.assertEqual(str(self.review), expected_output)

    def test_to_dict_method(self):
        """Test to_dict method includes Review attributes."""
        review_dict = self.review.to_dict()
        self.assertEqual(review_dict["__class__"], "Review")
        self.assertEqual(review_dict["text"], "Great place to stay!")

if __name__ == "__main__":
    unittest.main()
