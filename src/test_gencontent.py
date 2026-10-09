import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Recipe"
        title = extract_title(markdown)
        self.assertEqual(title, "Recipe")

    def test_extract_title_multiple_lines(self):
        markdown = "Some introduction\n# Recipe\nMore text"
        title = extract_title(markdown)
        self.assertEqual(title, "Recipe")

    def test_extract_title_raises_without_h1(self):
        markdown = "Some introduction\n## Subtitle"
        with self.assertRaises(Exception):
            extract_title(markdown)