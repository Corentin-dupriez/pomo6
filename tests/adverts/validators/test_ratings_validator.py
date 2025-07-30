from django.core.exceptions import ValidationError
from django.test import TestCase
from adverts.validators import RatingValidator

class RatingValidatorTest(TestCase):
    def test__creating_rating_above_5__raises_validation_error(self):
        validator = RatingValidator()
        with self.assertRaises(ValidationError) as e:
            validator(6)
        self.assertEqual(e.exception.message, 'The rating must be between 0 and 5')

    def test__creating_rating_below_0__raises_validation_error(self):
        validator = RatingValidator()
        with self.assertRaises(ValidationError) as e:
            validator(-1)
        self.assertEqual(e.exception.message, 'The rating must be between 0 and 5')