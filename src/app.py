from flask import Flask, jsonify, render_template
import os
import random
import string

app = Flask(__name__)

@app.route('/create_html_file', methods=['GET'])
def create_html_file():
    # Define the directory path
    directory_path = os.path.join('src', 'www', 'apps', 'ai-lms', 'templates')

    # Generate random filename with 4 alphabets
    filename = ''.join(random.choices(string.ascii_lowercase, k=4)) + '.html'

    # Create the HTML content
    html_content = render_template('index.html')

    # Write the HTML content to the file
    with open(os.path.join(directory_path, filename), 'w') as file:
        file.write(html_content)

    return jsonify({'message': 'HTML file created successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
