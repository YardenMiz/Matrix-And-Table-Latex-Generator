import unittest

from latexgrid import frac, matrix_latex, parse_block, table_latex


class TestFrac(unittest.TestCase):
    def test_simple_fraction(self):
        self.assertEqual(frac("1/2"), r"\frac{1}{2}")

    def test_letters_and_spaces(self):
        self.assertEqual(frac(" a / b "), r"\frac{a}{b}")

    def test_negative_sign_goes_in_front(self):
        self.assertEqual(frac("-3/4"), r"-\frac{3}{4}")

    def test_not_a_fraction_is_unchanged(self):
        for s in ["x", "2", r"\frac{1}{2}", "a/b/c", "1/", "/2", "x^2"]:
            self.assertEqual(frac(s), s.strip())


class TestMatrix(unittest.TestCase):
    def test_pmatrix(self):
        self.assertEqual(
            matrix_latex([["1", "2"], ["3", "4"]]),
            "\\begin{pmatrix}\n1 & 2 \\\\\n3 & 4\n\\end{pmatrix}",
        )

    def test_bracket_type(self):
        out = matrix_latex([["a"]], env="bmatrix")
        self.assertEqual(out, "\\begin{bmatrix}\na\n\\end{bmatrix}")

    def test_empty_cells_become_zero(self):
        self.assertEqual(
            matrix_latex([["", "1"], [" ", ""]]),
            "\\begin{pmatrix}\n0 & 1 \\\\\n0 & 0\n\\end{pmatrix}",
        )

    def test_fractions_converted(self):
        self.assertIn(r"\frac{1}{2} & -\frac{a}{b}", matrix_latex([["1/2", "-a/b"]]))


class TestTable(unittest.TestCase):
    def test_full_grid(self):
        self.assertEqual(
            table_latex([["א", "ב"], ["1", "2"]]),
            "\\begin{table}[h]\n\\centering\n\\begin{tabular}{|l|l|}\n\\hline\n"
            "א & ב \\\\ \\hline\n1 & 2 \\\\ \\hline\n"
            "\\end{tabular}\n\\end{table}",
        )

    def test_alignment_and_caption(self):
        out = table_latex([["x"]], align="c", caption="תוצאות")
        self.assertIn("\\begin{tabular}{|c|}", out)
        self.assertIn("\\end{tabular}\n\\caption{תוצאות}\n\\end{table}", out)

    def test_ampersand_escaped_but_math_kept(self):
        out = table_latex([["A & B", "$x^2$", r"already \& ok"]])
        self.assertIn(r"A \& B & $x^2$ & already \& ok \\", out)

    def test_empty_cells_stay_empty(self):
        self.assertIn(" &  \\\\ \\hline", table_latex([["", ""]]))


class TestParseBlock(unittest.TestCase):
    def test_tabs_and_newlines(self):
        self.assertEqual(parse_block("1\t2\n3\t4\n"), [["1", "2"], ["3", "4"]])

    def test_ragged_rows_padded(self):
        self.assertEqual(parse_block("1\t2\t3\n4"), [["1", "2", "3"], ["4", "", ""]])

    def test_windows_line_endings(self):
        self.assertEqual(parse_block("a\tb\r\nc\td"), [["a", "b"], ["c", "d"]])


if __name__ == "__main__":
    unittest.main()
