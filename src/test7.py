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



def read_array_items(array):
    for item in array:
        parts = item.split(":")  # Split the item by colon
        if len(parts) > 1:  # Check if there are modules after the item
            item_name = parts[0]  # First part is the item name
            modules = parts[1:]  # Remaining parts are modules
            for module in modules:
                print(item_name, module)


def create_article(Input):
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
    prompt_parts = [f"""You are An AI Expert on {Input}, start and end your code with <section class="docs-section" id="SEO OTPIMISED ID">,</section>your output is limited to html output not more than 500 words including code maximum 3000-4000 characters remmeber to end your code with </section> and start it with <section class="docs-section" id="SEO OTPIMISED ID">. HTML OUTPUT STRUCUTRE <section class="docs-section" id="SEO OTPIMISED ID"> you should start the html and end it with </section> . Do not try to give the complete html structure only this section.You can put code in <h5>Github Code Example:</h5> and it will look like code.DO NOT GIVE ANY OTHER HTML CODE. this is very short example you need to make a really really comprehsnisve module really long.{article_data} you have to write a complete module about {Input}, This is a complete module. No conculsion no ending as this is only a part of the topic.This is a major part of the course you need to make it as holistic as possible. do not include anything else than the {Input}.Keep it professional, crisp to the point and as accurate as possible. it should not be short.
    """]
    response = model.generate_content(prompt_parts)
    return response.text

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

def parse_array(array_string):
    # Assuming array_string is a string representation of a list
    # Remove the enclosing square brackets and split by comma
    array_elements = array_string.strip('[]').split(',')

    # Use json.loads to parse the array elements
    parsed_array = json.loads('[' + ','.join(array_elements) + ']')

    return parsed_array

t = create_article_data("python")
print(t)
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
max_attempts = 10

for article_id, article_content in reversed_articles:
    print("this is what we can use for article", article_id)
    for attempt in range(1, max_attempts + 1):
        try:
            t = create_article(article_id)
            weblink.insert_article_below_comment("<!-- add article below -->", t)
            break  # If successful, break out of the retry loop
        except Exception as e:
            print(f"Attempt {attempt} failed:", str(e))
            if attempt == max_attempts:
                print("Max attempts reached. Returning error.")
                # Handle error here if needed
                break  # Max attempts reached, move to the next article
            else:
                print("Retrying...")
                continue  # Retry the creation of the article

    # Continue to the next iteration of the loop
    continue




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


