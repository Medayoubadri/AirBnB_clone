#!/usr/bin/python3

"""
Unit tests for the Review class, sprinkled with humor and thoroughness.
"""

import unittest
import os
import json
from time import sleep
from datetime import datetime
from models.review import Review
from models import storage


class TestReview(unittest.TestCase):
    """Thorough tests for the Review class with some personality."""

    def setUp(self):
        """Sets up a Review instance before each test."""
        self.review = Review()
        self.review.place_id = "place_1234"
        self.review.user_id = "user_5678"
        self.review.text = "Amazing place! Just mind the raccoons."

    def tearDown(self):
        """Clean up any created files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    # Section 1: Tests for Instantiation
    def test_instance_creation(self):
        """Test creating a new Review instance without arguments."""
        self.assertIsInstance(self.review, Review)
        self.assertIn(self.review, storage.all().values())

    def test_unique_id_per_instance(self):
        """
        Test that each Review instance has a unique id.
        Because every opinion is special.
        """
        review2 = Review()
        self.assertNotEqual(self.review.id, review2.id)

    def test_id_is_string(self):
        """
        Test that id attribute is a string.
        A review without an ID is like a book without a cover.
        """
        self.assertIsInstance(self.review.id, str)

    def test_datetime_attributes(self):
        """
        Test that created_at and updated_at are datetime objects.
        Time ticks on, even for reviews.
        """
        self.assertIsInstance(self.review.created_at, datetime)
        self.assertIsInstance(self.review.updated_at, datetime)

    def test_different_created_at_for_multiple_instances(self):
        """
        Test different created_at times for distinct instances.
        Every review has its moment.
        """
        review2 = Review()
        sleep(0.01)
        review3 = Review()
        self.assertLess(review2.created_at, review3.created_at)

    def test_public_attributes(self):
        """
        Test that Review class has expected public attributes.
        Nothing but the truth here.
        """
        self.assertEqual(self.review.place_id, "place_1234")
        self.assertEqual(self.review.user_id, "user_5678")
        self.assertEqual(
            self.review.text, "Amazing place! Just mind the raccoons."
            )

    # Section 2: Tests for save Method
    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        old_updated_at = self.review.updated_at
        sleep(0.01)
        self.review.save()
        self.assertGreater(self.review.updated_at, old_updated_at)

    def test_save_creates_file(self):
        """
        Test that save() creates file.json.
        The review is saved, even if the experience is questionable.
        """
        self.review.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_content(self):
        """
        Test that save() writes correct data to file.json.
        Raccoons included.
        """
        self.review.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        key = f"Review.{self.review.id}"
        self.assertIn(key, data)
        self.assertEqual(
            data[key]["text"], "Amazing place! Just mind the raccoons."
            )

    def test_save_with_invalid_argument(self):
        """
        Test save() with an invalid argument raises a TypeError.
        No freeloaders allowed.
        """
        with self.assertRaises(TypeError):
            self.review.save(None)

    # Section 3: Tests for to_dict Method
    def test_to_dict_includes_all_attributes(self):
        """
        Test that to_dict() includes all Review attributes.
        Every detail matters.
        """
        review_dict = self.review.to_dict()
        self.assertIn("id", review_dict)
        self.assertIn("created_at", review_dict)
        self.assertIn("updated_at", review_dict)
        self.assertIn("place_id", review_dict)
        self.assertIn("user_id", review_dict)
        self.assertIn("text", review_dict)
        self.assertEqual(
            review_dict["text"], "Amazing place! Just mind the raccoons."
            )

    def test_to_dict_datetime_format(self):
        """
        Test that to_dict() converts datetime attributes to ISO format.
        Time, but make it stringy.
        """
        review_dict = self.review.to_dict()
        self.assertIsInstance(review_dict["created_at"], str)
        self.assertIsInstance(review_dict["updated_at"], str)
        self.assertEqual(
            review_dict["created_at"], self.review.created_at.isoformat()
            )
        self.assertEqual(
            review_dict["updated_at"], self.review.updated_at.isoformat()
            )

    def test_to_dict_additional_attributes(self):
        """
        Test that to_dict() includes dynamically added attributes.
        All feedback counts.
        """
        self.review.rating = 5  # Because who doesn't love stars?
        review_dict = self.review.to_dict()
        self.assertIn("rating", review_dict)
        self.assertEqual(review_dict["rating"], 5)

    def test_to_dict_with_invalid_argument(self):
        """
        Test that to_dict() with invalid arguments raises TypeError.
        This method is VIP-only.
        """
        with self.assertRaises(TypeError):
            self.review.to_dict(None)

    def test_to_dict_output(self):
        """
        Test that to_dict() output matches expected dictionary.
        All the details, down to the raccoons.
        """
        self.review.id = "123456"
        self.review.created_at = datetime(2024, 1, 1, 12, 0, 0)
        self.review.updated_at = datetime(2024, 1, 1, 12, 0, 0)
        expected_dict = {
            "id": "123456",
            "__class__": "Review",
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00",
            "place_id": "place_1234",
            "user_id": "user_5678",
            "text": "Amazing place! Just mind the raccoons.",
            "rating": 5
        }
        self.review.rating = 5
        self.assertEqual(self.review.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
