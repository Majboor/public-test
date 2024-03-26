import os
import os
import random
import string
import shutil
import subprocess

# Define the base directory path
BASE_DIR = "/workspace/apache-example/www/apps"

def generate_folder_name():
    """Generate a unique 4 alphabet folder name."""
    folder_name = ''.join(random.choices(string.ascii_lowercase, k=4))
    while os.path.exists(os.path.join(BASE_DIR, folder_name)):
        folder_name = ''.join(random.choices(string.ascii_lowercase, k=4))
    return folder_name

def clone_templ(clone_path,repo_url):
    """Clone a repo from the provided URL and move its files to the generated folder."""    
    os.makedirs(clone_path)
    print(clone_path)
    
    # Clone the repo
    subprocess.run(["git", "clone", repo_url, clone_path])

folder_name = generate_folder_name()   
clone_path = os.path.join(BASE_DIR, folder_name)
 
clone_templ(clone_path,'https://github.com/beginnerslvl/doc-template-main')

html_file = clone_path + '/index.html'
# print(html_file)

with open(html_file, "r", encoding="utf-8") as file:
    html_content = file.read()



class WebLink:
    def __init__(self, folder_name, html_content):
        self.folder_name = folder_name
        self.html_content = html_content
        self.folder_path = self.folder_name
        self.file_path = folder_name + '/index.html'
        print(self.file_path)
    
    def insert_article_below_comment(self, comment, article_content):
        with open(self.file_path, 'r') as file:
            html_content = file.read()
        
        # Find the index of the comment in the HTML content
        comment_index = html_content.find(comment)
        
        # If the comment exists, insert the article content below it
        if comment_index != -1:
            modified_content = html_content[:comment_index + len(comment)] + article_content + html_content[comment_index + len(comment):]
            with open(self.file_path, 'w') as file:
                file.write(modified_content)
            print("Article inserted successfully below the comment.")
        else:
            print("Comment not found. Article not inserted.")
        
        return self.file_path
    
    def add_header(self, header_content):
        with open(self.file_path, 'r') as file:
            html_content = file.read()
        
        # Find the index of the header comment
        header_comment_index = html_content.find("<!-- add header below -->")
        
        # If the header comment exists, insert the header content below it
        if header_comment_index != -1:
            modified_content = html_content[:header_comment_index + len("<!-- add header below -->")] + header_content + html_content[header_comment_index + len("<!-- add header below -->"):]
            with open(self.file_path, 'w') as file:
                file.write(modified_content)
            print("Header added successfully.")
        else:
            print("Header comment not found. Header not added.")
        
        return self.file_path

    def add_section(self, section_html):
        nav_start_index = self.html_content.find("<!-- nav here -->")
        nav_end_index = self.html_content.find("<!-- nav end -->")
        placeholder_index = self.html_content.find("<!-- Navigation links will be inserted here dynamically -->")

        if nav_start_index != -1 and nav_end_index != -1 and placeholder_index != -1:
            section_insert_index = nav_start_index + len("<!-- nav here -->")
            if placeholder_index > nav_start_index and placeholder_index < nav_end_index:
                section_insert_index = placeholder_index
            self.html_content = (self.html_content[:section_insert_index] +
                                 section_html +
                                 self.html_content[section_insert_index:])
            # Save the updated content into the file
            with open(self.file_path, 'w') as file:
                file.write(self.html_content)
        else:
            raise ValueError("Couldn't find navigation section or placeholders in HTML content.")

    def get_html_content(self):
        return self.html_content


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

weblink = WebLink(clone_path, html_content)

sections = [
    ("Introduction", ["Section Item 1.1", "Section Item 1.2"]),
    ("Chapter 1", ["Section Item 2.1", "Section Item 2.2"]),
    # Add more sections as needed
]
# adding ids
for section_title, section_items in sections:
    section_html = generate_section_html(section_title, section_items)
    weblink.add_section(section_html)


# print(weblink.get_html_content())

# adding header
header_content = """
<header class="docs-header">
  <h1 class="Introduction">Introduction <span class="docs-time">Secondary text</span></h1>
  <section id="docs-intro" class="docs-intro">
    <p>Section intro goes here. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque finibus
      condimentum nisl id vulputate. Praesent aliquet varius eros interdum suscipit. Donec eu purus sed nibh
      convallis bibendum quis vitae turpis. Duis vestibulum diam lorem, vitae dapibus nibh facilisis a. Fusce
      in malesuada odio.</p>
  </section>
 </header>
"""
weblink.add_header(header_content)

article_content = """
<article class="docs-article" id="section-item-1.1">
  <header class="docs-header">
    <h1 class="docs-heading">Python <span class="docs-time">Secondary text</span></h1>
  </header>
  <section class="docs-section" id="item-python-1">
    <h2 class="section-heading">Section Item Python 1</h2>
    <p>This is a new section added below the header.</p>
     <h5>Github Code Example:</h5>
  <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Illo, possimus quae error nulla et, distinctio facilis iusto consectetur ullam provident unde neque cumque obcaecati omnis ipsa corrupti magnam dolor minima.</p>
  <h5>Highlight.js Example:</h5>
  <p>Lorem ipsum dolor sit amet <a href="#">consectetur</a> adipisicing elit. Nihil laudantium ex quis. Velit ad quibusdam alias dolorum exercitationem molestiae, commodi repellat culpa soluta vitae? Incidunt ratione esse quisquam nam earum.</p>

  </section>  
</article>
"""

weblink.insert_article_below_comment("<!-- add article below -->", article_content)



# Example usage
