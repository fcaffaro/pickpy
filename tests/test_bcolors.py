import unittest
from enum import Enum
from pickpy.terminal import BColors


class TestBColors(unittest.TestCase):
    def test_is_enum_and_str(self):
        self.assertTrue(issubclass(BColors, Enum))
        self.assertTrue(issubclass(BColors, str))

    def test_values_are_ansi_sequences(self):
        # Verifica alcuni membri chiave
        self.assertTrue(BColors.OKGREEN.value.startswith("\033["))
        self.assertTrue(BColors.ENDC.value.startswith("\033["))
        self.assertIn("m", BColors.OKGREEN.value)
        self.assertIn("m", BColors.ENDC.value)

    def test_member_behaves_like_str(self):
        # I membri si comportano come stringhe nei confronti di uguaglianza
        self.assertTrue(isinstance(BColors.RED, str))
        self.assertEqual(BColors.RED, BColors.RED.value)
        self.assertEqual(BColors.OKBLUE + "Hello" + BColors.ENDC, BColors.OKBLUE.value + "Hello" + BColors.ENDC.value)


if __name__ == '__main__':
    unittest.main()
