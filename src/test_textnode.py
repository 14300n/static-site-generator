import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)
		
	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is also a text node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_url_not_eq(self):
		node_url = TextNode("Some text", TextType.LINK, "https://example.com")
		node_url2 = TextNode("Some text", TextType.LINK, None)
		self.assertNotEqual(node_url, node_url2)

	def test_texttype_not_eq(self):
		node_texttype = TextNode("This is written in BOLD", TextType.BOLD)
		node_texttype2 = TextNode("This is written in Italic", TextType.ITALIC)
		self.assertNotEqual(node_texttype, node_texttype2)

	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
		node = TextNode("This is a bold text node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a bold text node")

	def test_italic(self):
		node = TextNode("This is an italic text node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is an italic text node")

	def test_code(self):
		node = TextNode("This is a code text node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a code text node")

	def test_link(self):
		node = TextNode("Click here", TextType.LINK, "https://example.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "Click here")
		self.assertEqual(html_node.props, {"href": "https://example.com"})

	def test_image(self):
		node = TextNode("Click here", TextType.IMAGE, "https://example.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props, {"src": "https://example.com", "alt": "Click here"})


if __name__ == "__main__":
	unittest.main()
