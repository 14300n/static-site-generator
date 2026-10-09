import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

def test_markdown_to_blocks_multiple_blank_lines(self):
    md = """
First block here


Second block here
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "First block here",
            "Second block here",
        ],
    )

def test_markdown_to_blocks_leading_whitespace(self):
    md = """


First block here

Second block here


"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
         blocks,
         [
              "First block here",
              "Second block here",
         ],
    )

def test_markdown_to_blocks_single(self):
    md = """This is a block
that spans multiple lines
but has no blank lines"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
         blocks,
         [
              "This is a block\nthat spans multiple lines\nbut has no blank lines",
         ],
    )

def test_markdown_to_blocks_empty(self):
    md = ""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [],
    )


class TestMarkdownBlocks(unittest.TestCase):
    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
  
    def test_paragraph(self):
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = ">This is a quote\n>This is also a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_ulist(self):
        block = "- This is the start of an unordered list\n- This is the end of an unordered list."
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_olist(self):
        block = "1. This is the start of an ordered list\n2. This is the end of an ordered list."
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)