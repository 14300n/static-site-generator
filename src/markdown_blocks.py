from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        block = block.strip()
        if block == "":
            continue
        else:
            blocks.append(block)
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST    
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block_htmlnode = paragraph_to_html_node(block)
            children.append(block_htmlnode)
        elif block_type == BlockType.HEADING:
            block_htmlnode = heading_to_html_node(block)
            children.append(block_htmlnode)
        elif block_type == BlockType.CODE:
            block_htmlnode = code_to_html_node(block)
            children.append(block_htmlnode)
        elif block_type == BlockType.QUOTE:
            block_htmlnode = quote_to_html_node(block)
            children.append(block_htmlnode)
        elif block_type == BlockType.ULIST:
            block_htmlnode = ulist_to_html_node(block)
            children.append(block_htmlnode)
        elif block_type == BlockType.OLIST:
            block_htmlnode = olist_to_html_node(block)
            children.append(block_htmlnode)
    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [children])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        strip_line = line.lstrip(">").strip()
        new_lines.append(strip_line)
    joined_lines = " ".join(new_lines)
    children = text_to_children(joined_lines)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        strip_line = line[2:]
        children = text_to_children(strip_line)
        child_ulist = ParentNode("li", children)
        new_lines.append(child_ulist)
    return ParentNode("ul", new_lines)

def olist_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        parts = line.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


