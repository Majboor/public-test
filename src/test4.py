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

def clone_and_move_repo(repo_url):
    """Clone a repo from the provided URL and move its files to the generated folder."""
    folder_name = generate_folder_name()
    clone_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(clone_path)
    print(clone_path)
    
    # Clone the repo
    subprocess.run(["git", "clone", repo_url, clone_path])
    


if __name__ == "__main__":
    repo_url = input("Enter the URL of the repository: ")
    clone_and_move_repo(repo_url)
