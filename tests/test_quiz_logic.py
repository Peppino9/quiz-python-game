# tests/test_quiz_logic.py
import unittest
from quiz_logic import calculate_score

class TestQuizLogic(unittest.TestCase):
    """Test cases for the quiz_logic module."""

    def test_calculate_score_correct_answers(self):
        """Test calculating score with all correct answers."""
        answers = [{'question_index': 0, 'selected_option': 'France'},
                   {'question_index': 1, 'selected_option': 'Lionel Messi'}]
        self.assertEqual(calculate_score(answers), 2)

    def test_calculate_score_incorrect_answers(self):
        """Test calculating score with all incorrect answers."""
        answers = [{'question_index': 0, 'selected_option': 'Brazil'},
                   {'question_index': 1, 'selected_option': 'Cristiano Ronaldo'}]
        self.assertEqual(calculate_score(answers), 0)

if __name__ == '__main__':
    unittest.main()