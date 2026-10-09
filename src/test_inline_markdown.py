import unittest
from textnode import TextNode, TextType
from inline_markdown import MarkdownSyntaxError, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("The **loud** cars outside.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode('The ', TextType.TEXT),
                TextNode('loud', TextType.BOLD),
                TextNode(' cars outside.', TextType.TEXT)
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("We could use a `print` call.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode('We could use a ', TextType.TEXT),
                TextNode('print', TextType.CODE),
                TextNode(' call.', TextType.TEXT)
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This will show _two_ separate _things_.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode('This will show ', TextType.TEXT),
                TextNode('two', TextType.ITALIC),
                TextNode(' separate ', TextType.TEXT),
                TextNode('things', TextType.ITALIC),
                TextNode('.', TextType.TEXT)
            ],
            new_nodes,
        )

    def test_delim_bold_leading(self):
        node = TextNode("**Loud** cars outside.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Loud", TextType.BOLD),
                TextNode(" cars outside.", TextType.TEXT)
            ],
            new_nodes
        )

    def test_non_text_passthrough(self):
        node = TextNode("Lets see if there is **something** here.", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Lets see if there is **something** here.", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_unbalanced_delimiter(self):
        node = TextNode("Lets see an **opening and no closing.", TextType.TEXT)
        with self.assertRaises(MarkdownSyntaxError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://wikipedia.org"),
            ],
            matches,
        )

    def test_extract_markdown_images_multiple(self):
        text = "Here is ![one](https://example.com/1.png) and ![two](https://example.com/2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("one", "https://example.com/1.png"),
                ("two", "https://example.com/2.png"),
            ],
            matches,
        )

    def test_extract_markdown_links_ignores_images(self):
        text = "This is a link [website](https://example.com) and an image ![pic](https://example.com/pic.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("website", "https://example.com"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode(
            "![alt text](https://example.com/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
            ],
            new_nodes
        )

    def test_delim_no_limiter(self):
        node = TextNode("This is just plain text with no markdown.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is just plain text with no markdown.", TextType.TEXT)
            ],
            new_nodes
        )

    def test_delim_mutliple_nodes(self):
        nodes = [
            TextNode("Some **bold** text.", TextType.TEXT),
            TextNode("Plain text with nothing special.", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
                TextNode("Plain text with nothing special.", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_images_no_image(self):
        node = TextNode("Just a plain text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Just a plain text with no images.", TextType.TEXT)
            ],
            new_nodes
        )

    def test_extract_markdown_images_ignores_links(self):
        text = "This is a link [website](https://example.com) and a image ![pic](https://example.com/pic.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("pic", "https://example.com/pic.png"),
            ],
            matches
        )

    def test_split_images_leading_image(self):
        node = TextNode(
            "![alt](https://example.com/image.png) trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_images_trailing_image(self):
        node = TextNode(
            "leading text ![alt](https://example.com/image.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("leading text ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://example.com/image.png"),
            ],
            new_nodes
        )

    def test_split_links_ignores_images(self):
        node = TextNode(
            "This is an ![image](https://example.com/img.png) and a [link](https://example.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is an ![image](https://example.com/img.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_image(self):
        text = "This is text with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
        )

    def test_text_to_textnodes_link(self):
        text = "This is text with a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
        )

if __name__ == "__main__":
    unittest.main()