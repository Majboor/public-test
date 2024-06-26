import os
import os
import random
import string
import shutil
import subprocess
import google.generativeai as genai
import json
genai.configure(api_key="AIzaSyBKQQq8CLYwz_1Hogh-cGvy5gqk8l5uU8k")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


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



weblink = WebLink(clone_path, html_content)



def generate_section_html(section_title, section_items):
    section_html = f"""
    <li class="nav-item section-title">
        <a class="nav-link scrollto" href="#{section_title.lower().replace(' ', '-')}-section">{section_title}</a>
        <ul class="nav flex-column mt-2 lvl2">
    """
    for item_title in section_items:
        # Extract item name and modules
        item_name, *modules = item_title.split(':')
        for module in modules:
            # Generate href and section id for each module
            module_id = f"{item_name.lower().replace(' ', '-')}-{module.strip().lower().replace(' ', '-')}"
            section_html += f"""
            <li class="nav-item">
                <a class="nav-link scrollto" href="#{module_id}">{item_title}</a>
            </li>
            """
    section_html += """
        </ul>
    </li>
    """
    return section_html

def generate_sections_from_functionx_array(functionx_array,article_data):
    sections = []
    articles = []
    for item in functionx_array:
        title, *modules = item.split(':')
        section_title = title.strip()
        section_items = [f"{section_title}: {module}" for module in modules]
        sections.append((section_title, section_items))
        # Generate article content for each section item
        for index, section_item in enumerate(section_items, start=1):
            # Extract the last module as part of the section ID
            last_module = section_item.split(':')[-1].strip().lower().replace(' ', '-')
            # Generate article ID based on the section title and the last module
            article_id = f"{section_title.replace(' ', '-').lower()}-{last_module}"
            article_content = f"""
<article class="docs-article" id="{article_id}">
  <header class="docs-header">
    <h1 class="docs-heading">{section_title} <span class="docs-time">Secondary text</span></h1>
  </header>
{article_data} 
</article>
"""
            articles.append((article_id, article_content))  # Store article ID and content
    return sections, articles





def create_article_data(Input):
    prompt_parts = ["The user wants a presentation about " + Input]
    response = model.generate_content(prompt_parts)
    return response.text


article_data = """
  <section class="docs-section" id="{last_module}">
    <h2 class="section-heading">{section_item}</h2>
    <p>This is a new section added below the header.</p>
    <h5>Github Code Example:</h5>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Illo, possimus quae error nulla et, distinctio facilis iusto consectetur ullam provident unde neque cumque obcaecati omnis ipsa corrupti magnam dolor minima.</p>
    <h5>Highlight.js Example:</h5>
    <p>Lorem ipsum dolor sit amet <a href="#">consectetur</a> adipisicing elit. Nihil laudantium ex quis. Velit ad quibusdam alias dolorum exercitationem molestiae, commodi repellat culpa soluta vitae? Incidunt ratione esse quisquam nam earum.</p>
  </section>  
"""

import google.generativeai as genai
genai.configure(api_key="AIzaSyBKQQq8CLYwz_1Hogh-cGvy5gqk8l5uU8k")
import json
# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)



def read_array_items(array):
    for item in array:
        parts = item.split(":")  # Split the item by colon
        if len(parts) > 1:  # Check if there are modules after the item
            item_name = parts[0]  # First part is the item name
            modules = parts[1:]  # Remaining parts are modules
            for module in modules:
                print(item_name, module)


def create_article_data(Input):
    prompt_parts = [f""" 
    You are an AI Teacher for {Input} you are required to teach the student {Input}.Your outputs are limited to an array format. 
Each element in the array represents a Course.
Within each element (Course), there are multiple segments separated by colons.
The first segment in each element represents the course itself, followed by three modules (module1, module2, and module3) associated with that course.
For example:

The first element in the array is "Basics of python:module1:module2:module3".
Here, "Basics of python" is the item, and "module1", "module2", and "module3" are associated modules for this item.
Similarly, the second element is "if conditions:module1:module2:module3", and so on.
[
    "item1:module1:module2:module3",
    "item2:module1:module2:module3",
    "item3:module1:module2:module3",
    "item4:module1:module2:module3"
]
Now you are required to return an array.Only return an array nothing else. This array should consist of a proper syllabus in proper order.As a basic rule the starter modules and topics are supposed to be easier then we have more and more difficult modules. 
each topic in the array will look like this
 "item1:module1:module2:module3",
MAX LIMIT OF TOPICS:10
MAX LIMIT OF MODULES:5 in each topic
each topic should have a minimum of three modules
module and topic both should be less than 5 words
topics should be based on strategic learning so that at the end of the course the student is aware of {Input}. They should be like a ride, starting from beginning of {Input}  then passively difficult {Input}. it should have complete modules not written like module1 module2 
    
    """]
    response = model.generate_content(prompt_parts)
    return response.text
t = create_article_data("python")
print(t)


def parse_array(array_string):
    # Assuming array_string is a string representation of a list
    # Remove the enclosing square brackets and split by comma
    array_elements = array_string.strip('[]').split(',')

    # Use json.loads to parse the array elements
    parsed_array = json.loads('[' + ','.join(array_elements) + ']')

    return parsed_array

functionx_array = parse_array(t)
print(functionx_array)


read_array_items(functionx_array)








sections, articles = generate_sections_from_functionx_array(functionx_array,article_data)

for section_title, section_items in sections:
    section_html = generate_section_html(section_title, section_items)
    weblink.add_section(section_html)

# Insert articles below the comment
# Reverse the articles list
reversed_articles = reversed(articles)

# Insert articles below the comment in reverse order
for article_id, article_content in reversed_articles:
    weblink.insert_article_below_comment("<!-- add article below -->", article_content)



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

# article_content = """
# <article class="docs-article" id="section-item-1.1">
#   <header class="docs-header">
#     <h1 class="docs-heading">Python <span class="docs-time">Secondary text</span></h1>
#   </header>
#   <section class="docs-section" id="item-python-1">
#     <h2 class="section-heading">Section Item Python 1</h2>
#     <p>This is a new section added below the header.</p>
#      <h5>Github Code Example:</h5>
#   <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Illo, possimus quae error nulla et, distinctio facilis iusto consectetur ullam provident unde neque cumque obcaecati omnis ipsa corrupti magnam dolor minima.</p>
#   <h5>Highlight.js Example:</h5>
#   <p>Lorem ipsum dolor sit amet <a href="#">consectetur</a> adipisicing elit. Nihil laudantium ex quis. Velit ad quibusdam alias dolorum exercitationem molestiae, commodi repellat culpa soluta vitae? Incidunt ratione esse quisquam nam earum.</p>

#   </section>  
# </article>
# """

# weblink.insert_article_below_comment("<!-- add article below -->", article_content)



# Example usage
