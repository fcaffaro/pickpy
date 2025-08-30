import os
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import builtins

from pickpy.terminal import Terminal, BColors
from pickpy.menu import TerminalMenu


class TestTerminal(unittest.TestCase):
    def test_sanitize_removes_ansi_and_control_chars(self):
        term = Terminal()
        text = "\033[31mHello\x07World\n"
        clean = term.sanitize(text)
        self.assertNotIn("\033", clean)
        self.assertNotIn("\x07", clean)
        self.assertTrue(clean.endswith("World\n"))

    def test_colorize_with_enum_when_supported(self):
        term = Terminal()
        with patch.object(Terminal, 'supports_color', return_value=True):
            out = term.colorize("Hello", BColors.OKGREEN)
            self.assertEqual(out, f"{BColors.OKGREEN.value}Hello{BColors.ENDC.value}")

    def test_colorize_with_str_when_supported(self):
        term = Terminal()
        with patch.object(Terminal, 'supports_color', return_value=True):
            out = term.colorize("Hello", "\033[92m")
            self.assertEqual(out, f"\033[92mHello{BColors.ENDC.value}")

    def test_colorize_when_not_supported(self):
        term = Terminal()
        with patch.object(Terminal, 'supports_color', return_value=False):
            out = term.colorize("Hello", BColors.OKGREEN)
            self.assertEqual(out, "Hello")

    def test_safe_print_sanitizes_and_prints(self):
        term = Terminal()
        buf = io.StringIO()
        with redirect_stdout(buf):
            term.safe_print("\033[31mRed\x07Text")
        self.assertEqual(buf.getvalue(), "RedText\n")

    def test_supports_color_env_override(self):
        with patch.dict(os.environ, {"PICKPY_COLOR": "1"}, clear=False):
            self.assertTrue(Terminal().supports_color())
        with patch.dict(os.environ, {"PICKPY_COLOR": "0"}, clear=False):
            self.assertFalse(Terminal().supports_color())

    def test_clear_terminal_fallback_when_not_interactive(self):
        term = Terminal()
        with patch.object(Terminal, 'is_interactive', return_value=False):
            with patch.dict(os.environ, {"PYCHARM_HOSTED": ""}, clear=False):
                buf = io.StringIO()
                with redirect_stdout(buf):
                    term.clear_terminal()
        out = buf.getvalue()
        self.assertGreaterEqual(out.count("\n"), 50)


class TestMenu(unittest.TestCase):
    def test_get_choice_applies_colors(self):
        menu = TerminalMenu()
        # Forza colori supportati
        with patch.object(Terminal, 'supports_color', return_value=True):
            # Simula input utente "1"
            with patch.object(builtins, 'input', return_value='1'):
                buf = io.StringIO()
                with redirect_stdout(buf):
                    choice = menu.get_choice(
                        ['A', 'B'],
                        header='Header',
                        header_color=BColors.OKBLUE,
                        option_color=BColors.OKGREEN,
                        error_color=BColors.FAIL,
                    )
        out = buf.getvalue()
        # Verifica che header e opzioni siano colorati
        self.assertIn(BColors.OKBLUE.value + 'Header' + BColors.ENDC.value, out)
        self.assertIn(BColors.OKGREEN.value + '1. A' + BColors.ENDC.value, out)
        self.assertIn(BColors.OKGREEN.value + '2. B' + BColors.ENDC.value, out)
        self.assertEqual(choice, 'A')

    def test_select_option_fallback_forwards_unselected_as_option_color(self):
        menu = TerminalMenu()
        menu.terminal.is_interactive = lambda: False
        with patch.object(menu, 'get_choice', return_value='B') as mocked:
            choice = menu.select_option(['A', 'B', 'C'], header='Header', header_color=BColors.WARNING, unselected_color=BColors.CYAN)
        self.assertEqual(choice, 'B')
        # Controlla che i kwargs includano header_color e option_color
        kwargs = mocked.call_args.kwargs
        self.assertEqual(kwargs.get('header_color'), BColors.WARNING)
        self.assertEqual(kwargs.get('option_color'), BColors.CYAN)


if __name__ == '__main__':
    unittest.main()
