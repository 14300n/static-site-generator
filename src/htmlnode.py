
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props != None:
            prop_string = ""
            for prop, value  in self.props.items():
                prop_string += f' {prop}="{value}"'
            return prop_string
        else:
            return ""
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)
    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag found.")
        elif self.children == None:
            raise ValueError("No children found.")
        else:
            parent_node = ""
            for child in self.children:
                child = child.to_html()
                parent_node += (child)
            return f'<{self.tag}{self.props_to_html()}>{parent_node}</{self.tag}>'



    