from textnode import TextNode, TextType
import re

class MarkdownSyntaxError(Exception):
    def __init__(self, delimiter, text):
        self.delimiter = delimiter
        self.text = text
        super().__init__(f"unbalanced delimiter {delimiter!r} in: {text!r}")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise MarkdownSyntaxError(delimiter, node.text)
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        else:
            images = extract_markdown_images(node.text)
            if not images:
                result.append(node)
                continue
        remaining_text = node.text
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            sections = remaining_text.split(image_markdown, 1)
            if sections[0]:
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text = sections[1]
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        else:
            links = extract_markdown_links(node.text)
            if not links:
                result.append(node)
                continue
        remaining_text = node.text
        for alt_text, url in links:
            link_markdown = f"[{alt_text}]({url})"
            sections = remaining_text.split(link_markdown, 1)
            if sections[0]:
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(alt_text, TextType.LINK, url))
            remaining_text = sections[1]
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    return result

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^()]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    

