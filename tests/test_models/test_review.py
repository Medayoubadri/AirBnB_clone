#!/usr/bin/python3
"""
Unit tests for the Review class.
"""

import unittest
import os
from time import sleep
from datetime import datetime
from models.review import Review
from models import storage


class TestReviewInstantiation(unittest.TestCase):
    """Tests for the instantiation of the Review class."""

    def setUp(self):
        """Sets up a Review instance before each test."""
        self.review = Review()

    def tearDown(self):
        """Clean up any created files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_no_args_instantiates(self):
        """Test instantiating without arguments."""
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        """Test that a new Review instance is stored in objects."""
        self.assertIn(self.review, storage.all().values())

    def test_id_is_public_str(self):
        """Test that id is a public string attribute."""
        self.assertEqual(str, type(self.review.id))

    def test_datetime_attributes(self):
        """Test that created_at and updated_at are datetime objects."""
        self.assertEqual(datetime, type(self.review.created_at))
        self.assertEqual(datetime, type(self.review.updated_at))

    def test_place_id_is_public_class_attribute(self):
        """Test that place_id is a public class attribute."""
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(self.review))
        self.assertNotIn("place_id", self.review.__dict__)

    def test_user_id_is_public_class_attribute(self):
        """Test that user_id is a public class attribute."""
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(self.review))
        self.assertNotIn("user_id", self.review.__dict__)

    def test_text_is_public_class_attribute(self):
        """Test that text is a public class attribute."""
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(self.review))
        self.assertNotIn("text", self.review.__dict__)

    def test_str_representation(self):
        """Test the string representation of a Review instance."""
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
        """Test instantiating with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)


class TestReviewSave(unittest.TestCase):
    """Tests for the save method of the Review class."""

    def setUp(self):
        """Set up a Review instance before testing."""
        self.review = Review()

    def tearDown(self):
        """Clean up after testing."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        old_updated_at = self.review.updated_at
        sleep(0.01)
        self.review.save()
        self.assertGreater(self.review.updated_at, old_updated_at)

    def test_save_creates_file(self):
        """Test that save() creates a file.json."""
        self.review.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_with_invalid_argument(self):
        """Test save() raises TypeError with invalid arguments."""
        with self.assertRaises(TypeError):
            self.review.save(None)

    def test_save_updates_file(self):
        """Test that save() updates the content of file.json."""
        self.review.save()
        review_id = "Review." + self.review.id
        with open("file.json", "r") as f:
            self.assertIn(review_id, f.read())


class TestReviewToDict(unittest.TestCase):
    """Tests for the to_dict method of the Review class."""

    def setUp(self):
        """Set up a Review instance for testing."""
        self.review = Review()

    def tearDown(self):
        """Clean up after testing."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_to_dict_type(self):
        """Test that to_dict() returns a dictionary."""
        self.assertTrue(dict, type(self.review.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that to_dict() includes all expected keys."""
        review_dict = self.review.to_dict()
        self.assertIn("id", review_dict)
        self.assertIn("created_at", review_dict)
        self.assertIn("updated_at", review_dict)
        self.assertIn("__class__", review_dict)

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that datetime attributes are converted to strings in to_dict()."""
        review_dict = self.review.to_dict()
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict()."""
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

    def test_to_dict_with_additional_attributes(self):
        """Test to_dict() includes dynamically added attributes."""
        self.review.rating = 5
        review_dict = self.review.to_dict()
        self.assertIn("rating", review_dict)
        self.assertEqual(review_dict["rating"], 5)


if __name__ == "__main__":
    unittest.main()
