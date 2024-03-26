# Define the functionx array
functionx_array = [
    "item1:module1:module2:module3",
    "item2:module1:module2:module3",
    "item3:module1:module2:module3",
    "item4:module1:module2:module3"
]

# Define the sections data array
sections = [
    ("Introduction", ["Section Item 1.1", "Section Item 1.2"]),
    ("Chapter 1", ["Section Item 2.1", "Section Item 2.2"]),
    # Add more sections as needed
]
# Function to generate HTML content for each item in functionx_array
def generate_html_content(item, modules):
    html_content = f"""
<article class="docs-article" id="section-{item}">
  <header class="docs-header">
    <h1 class="docs-heading">{item} <span class="docs-time">Secondary text</span></h1>
  </header>
"""
    for module in modules:
        html_content += f"""  <section class="docs-section" id="{module}-{item}">
    <h2 class="section-heading">Section Item {module}</h2>
    <p>This is a new section added below the header for {module}.</p>
  </section>"""
    html_content += "\n</article>\n"
    return html_content

# Iterate over functionx_array and generate HTML content for each item
for i, item in enumerate(functionx_array):
    item_id, *modules = item.split(":")
    html_content = generate_html_content(item_id, modules)
    print(html_content)
    sections.append((item_id, [f"Section Item {module}" for module in modules]))

# Now sections array is updated with entries based on functionx_array
print(sections)
