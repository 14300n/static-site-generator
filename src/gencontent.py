import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No header found.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path) as f:
        from_path_read = f.read()
    with open(template_path) as f:
        template_path_read = f.read()
    from_path_html = markdown_to_html_node(from_path_read).to_html()
    from_path_title = extract_title(from_path_read)
    replace_title = template_path_read.replace("{{ Title }}", from_path_title)
    replace_content = replace_title.replace("{{ Content }}", from_path_html)
    replace_href = replace_content.replace('href="/', 'href="' + basepath)
    replace_src = replace_href.replace('src="/', 'src="' + basepath)
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(replace_src)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, filename)
        target_dest_path = os.path.join(dest_dir_path, filename)
        source_path_check = os.path.isfile(source_path)
        if source_path_check:
            html_path = Path(target_dest_path).with_suffix(".html")
            generate_page(source_path, template_path, html_path, basepath)
        else:
            generate_pages_recursive(source_path, template_path, target_dest_path, basepath)










