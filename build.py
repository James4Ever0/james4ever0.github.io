# render README.md into index.html
import markdown
from jinja2 import Environment, FileSystemLoader

# Markdown content
markdown_content = open("README.md").read()
verification = open("verification.txt").read()

# Convert Markdown to HTML
html_content = markdown.markdown(markdown_content)

# Load the template from file
file_loader = FileSystemLoader(
    "."
)  # Replace 'path_to_templates_directory' with the actual path
env = Environment(loader=file_loader)
template = env.get_template(
    "index.html.j2"
)  # Replace 'sitemap_template.html' with the actual template file name

# Render the template with the data
rendered_template = template.render(content=html_content, verification=verification)

print("Template rendered.")

# Write the template content to a file
with open("index.html", "w+", encoding="utf-8") as file:
    file.write(rendered_template)

print("Markdown converted to HTML and written to index.html")
