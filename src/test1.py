# Define the Navbar class
class Navbar:
    def __init__(self, html_content):
        self.html_content = html_content
        self.nav_start = '<!-- nav here -->'
        self.nav_end = '<!-- nav end -->'
        self.section_placeholder = '<!-- Navigation links will be inserted here dynamically -->'

    def add_section(self, section_html):
        nav_start_index = self.html_content.find(self.nav_start)
        nav_end_index = self.html_content.find(self.nav_end)
        placeholder_index = self.html_content.find(self.section_placeholder)

        if nav_start_index != -1 and nav_end_index != -1 and placeholder_index != -1:
            section_insert_index = nav_start_index + len(self.nav_start)
            if placeholder_index > nav_start_index and placeholder_index < nav_end_index:
                section_insert_index = placeholder_index
            self.html_content = (self.html_content[:section_insert_index] +
                                 section_html +
                                 self.html_content[section_insert_index:])
        else:
            raise ValueError("Couldn't find navigation section or placeholders in HTML content.")

    def get_html_content(self):
        return self.html_content

# Example usage:
nav_content = """
<!-- nav here -->
<div id="docs-sidebar" class="docs-sidebar">
<div class="top-search-box d-lg-none p-3">
<form class="search-form">
<input type="text" placeholder="Search the docs..." name="search" class="form-control search-input">
<button type="submit" class="btn search-btn" value="Search">
<i class="fas fa-search"></i>
</button>
</form>
</div>
<nav id="docs-nav" class="docs-nav navbar">
<ul class="section-items list-unstyled nav flex-column pb-3">
<!-- Navigation links will be inserted here dynamically -->
</ul>
</nav>
</div>
<!-- nav end -->
"""

navbar = Navbar(nav_content)

# Function to generate section HTML
def generate_section_html(section_title, section_items):
    section_html = f"""
    <li class="nav-item section-title">
        <a class="nav-link scrollto" href="#{section_title.lower().replace(' ', '-')}">{section_title}</a>
        <ul class="nav flex-column mt-2 lvl2">
    """
    for item_title in section_items:
        section_html += f"""
            <li class="nav-item">
                <a class="nav-link scrollto" href="#{item_title.lower().replace(' ', '-')}">{item_title}</a>
            </li>
        """
    section_html += """
        </ul>
    </li>
    """
    return section_html

# Adding custom sections
sections = [
    ("Introduction", ["Section Item 1.1", "Section Item 1.2"]),
    ("Chapter 1", ["Section Item 2.1", "Section Item 2.2"]),
    # Add more sections as needed
]

for section_title, section_items in sections:
    section_html = generate_section_html(section_title, section_items)
    navbar.add_section(section_html)

# Print the updated HTML content
# print(navbar.get_html_content())
