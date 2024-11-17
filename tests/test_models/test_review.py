#!/usr/bin/python3
"""
Unit tests for the Review class.
"""

import unittest
import os
import json
from time import sleep
from datetime import datetime
from models.review import Review
from models import storage


class TestReviewInstantiation(unittest.TestCase):
    """Thorough and witty tests for Review instantiation."""

    def setUp(self):
        """Sets up a fresh Review instance before each test."""
        self.review = Review()

    def tearDown(self):
        """Cleans up any mess after a test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_instance_creation(self):
        """Test creating a Review instance. Did it even happen?"""
        self.assertIsInstance(self.review, Review)
        self.assertIn(self.review, storage.all().values())

    def test_unique_id_per_instance(self):
        """
        Test that each Review has its own ID.
        Like snowflakes, but less cold.
        """
        review2 = Review()
        self.assertNotEqual(self.review.id, review2.id)

    def test_id_is_string(self):
        """Check if the ID is a string. Integer IDs are so last year."""
        self.assertIsInstance(self.review.id, str)

    def test_datetime_attributes(self):
        """Verify that created_at and updated_at are datetime objects."""
        self.assertIsInstance(self.review.created_at, datetime)
        self.assertIsInstance(self.review.updated_at, datetime)

    def test_different_created_at_for_multiple_instances(self):
        """Ensure created_at timestamps differ for different instances. Time moves on."""
        review2 = Review()
        sleep(0.01)
        review3 = Review()
        self.assertLess(review2.created_at, review3.created_at)

    def test_public_class_attributes(self):
        """Confirm public class attributes are in place but not instance-specific."""
        self.assertIn("place_id", dir(self.review))
        self.assertNotIn("place_id", self.review.__dict__)
        self.assertIn("user_id", dir(self.review))
        self.assertNotIn("user_id", self.review.__dict__)
        self.assertIn("text", dir(self.review))
        self.assertNotIn("text", self.review.__dict__)

    def test_str_representation(self):
        """Test the string representation. Is it charming enough?"""
        dt = datetime.today()
        dt_repr = repr(dt)
        self.review.id = "123456"
        self.review.created_at = self.review.updated_at = dt
        review_str = self.review.__str__()
        self.assertIn("[Review] (123456)", review_str)
        self.assertIn("'id': '123456'", review_str)
        self.assertIn("'created_at': " + dt_repr, review_str)
        self.assertIn("'updated_at': " + dt_repr, review_str)

    def test_instantiation_with_kwargs(self):
        """Test instantiating with keyword arguments. Cheating, are we?"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)


class TestReviewSave(unittest.TestCase):
    """Testing the save method like it's a bestseller."""

    def setUp(self):
        """Set up the drama before testing save()."""
        self.review = Review()

    def tearDown(self):
        """Clean up the stage after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_save_updates_updated_at(self):
        """Test save() updates updated_at. It better be punctual."""
        old_updated_at = self.review.updated_at
        sleep(0.01)
        self.review.save()
        self.assertGreater(self.review.updated_at, old_updated_at)

    def test_save_creates_file(self):
        """Test save() creates the sacred file.json. It’s canon."""
        self.review.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_with_invalid_argument(self):
        """Try saving with invalid arguments. Spoiler: it’ll fail."""
        with self.assertRaises(TypeError):
            self.review.save(None)

    def test_save_updates_file_content(self):
        """Test save() actually writes correct data. No half-measures."""
        self.review.save()
        review_id = f"Review.{self.review.id}"
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn(review_id, data)
        self.assertEqual(data[review_id]["__class__"], "Review")


class TestReviewToDict(unittest.TestCase):
    """Because dictionaries are cool and to_dict() deserves attention."""

    def setUp(self):
        """Set up a Review instance for testing dictionary conversion."""
        self.review = Review()

    def tearDown(self):
        """Sweep up after testing."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_to_dict_type(self):
        """Does to_dict() return a dictionary? Or is it faking it?"""
        self.assertTrue(dict, type(self.review.to_dict()))

    def test_to_dict_contains_expected_keys(self):
        """Does the dictionary have all the juicy details?"""
        review_dict = self.review.to_dict()
        self.assertIn("id", review_dict)
        self.assertIn("created_at", review_dict)
        self.assertIn("updated_at", review_dict)
        self.assertIn("__class__", review_dict)

    def test_to_dict_datetime_attributes_are_strs(self):
        """Make sure datetime fields are stringified in ISO format."""
        review_dict = self.review.to_dict()
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_with_additional_attributes(self):
        """Dynamic attributes in the dictionary? Yes, please."""
        self.review.rating = 5
        review_dict = self.review.to_dict()
        self.assertIn("rating", review_dict)
        self.assertEqual(review_dict["rating"], 5)

    def test_to_dict_output(self):
        """Check if to_dict() output matches expectations."""
        dt = datetime.today()
        self.review.id = "123456"
        self.review.created_at = self.review.updated_at = dt
        expected_dict = {
            "id": "123456",
            "__class__": "Review",
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat(),
        }
        self.assertDictEqual(self.review.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
