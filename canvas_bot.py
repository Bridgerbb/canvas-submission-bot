import os
import requests
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
TOKEN = os.getenv("CANVAS_API_TOKEN")
BASE_URL = "https://boisestatecanvas.instructure.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def get_paginated_data(url, params=None):
    """Helper function to handle Canvas API pagination."""
    results = []
    
    # Loop to keep requesting the 'next' page until there are no more pages
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            break
            
        results.extend(response.json())
        
        # Canvas puts the URL for the next page in the 'Link' header
        # The requests library automatically parses this into response.links
        url = response.links.get('next', {}).get('url')
        
        # Parameters are already included in the 'next' URL, so we clear them
        params = None 
        
    return results

def list_active_courses():
    """Fetches and prints active courses."""
    print("\nFetching your active courses...")
    url = f"{BASE_URL}/courses"
    params = {"enrollment_state": "active", "enrollment_type": "student"}
    
    courses = get_paginated_data(url, params)
    
    print("\n--- Your Active Courses ---")
    for course in courses:
        if 'name' in course:
            print(f"ID: {course['id']} | Name: {course['name']}")

def list_assignments(course_id):
    """Fetches and prints assignments for a specific course."""
    print(f"\nFetching assignments for course {course_id}...")
    url = f"{BASE_URL}/courses/{course_id}/assignments"
    
    assignments = get_paginated_data(url)
    
    print(f"\n--- Assignments for Course {course_id} ---")
    for item in assignments:
        print(f"ID: {item['id']} | Name: {item['name']}")

def submit_github_url(course_id, assignment_id, repo_url):
    """Submits a URL to a specific Canvas assignment."""
    print(f"\nSubmitting {repo_url} to Canvas...")
    url = f"{BASE_URL}/courses/{course_id}/assignments/{assignment_id}/submissions"
    
    # This payload tells Canvas we are submitting a website URL
    data = {
        "submission[submission_type]": "online_url",
        "submission[url]": repo_url
    }
    
    response = requests.post(url, headers=HEADERS, data=data)
    
    if response.status_code == 201:
        print("\n✅ SUCCESS! Your URL has been submitted!")
    else:
        print(f"\n❌ Failed to submit. Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    if not TOKEN:
        print("Error: CANVAS_API_TOKEN not found. Please check your .env file.")
    else:
        # 1. Print courses
        list_active_courses()
        
        # 2. Get user input for the course
        c_id = input("\nEnter the Course ID you want to look at: ")
        
        # 3. Print assignments for that course
        list_assignments(c_id)
        
        # 4. Get user input for the assignment and the URL
        a_id = input("\nEnter the Assignment ID you want to submit to: ")
        github_url = input("Enter your public URL: ")
        
        # 5. Final confirmation before submitting
        print(f"\nYou are about to submit: {github_url}")
        confirm = input(f"Submit to assignment {a_id}? (y/n): ")
        
        if confirm.lower() == 'y':
            submit_github_url(c_id, a_id, github_url)
        else:
            print("Submission cancelled. Phew, that was a close one!")