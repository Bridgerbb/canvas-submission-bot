Canvas Submission Bot

A command-line interface tool built in Python to help students interact with the Canvas LMS REST API. This tool allows users to view their active courses, list assignments, and submit project URLs directly from the terminal, simplifying the workflow for developers who prefer the console over a web browser.

![Demo](assets/demo.gif)

Setup Instructions
1. Prerequisites
Python 3.x must be installed on your system.

A valid Canvas Access Token is required to authenticate with the API.

2. Clone the Repository
Open your terminal and clone your repo: git clone <your-repo-url>

Navigate into the directory: cd canvas-submission-bot

3. Install Dependencies
This project uses the requests library for HTTP communication and python-dotenv for managing secrets.

Run this command: pip install requests python-dotenv

4. Configure Environment Variables
In the root directory, create a file named .env.

Add your Canvas API token to this file like this: CANVAS_API_TOKEN=your_token_here

Security Warning: Ensure your .env file is never committed to GitHub. A .env.example file is provided to show the required format without exposing your secret token.

5. Running the Tool
Execute the script using Python: python canvas_bot.py

Example Usage
Listing Courses and Assignments
The tool first fetches your active enrollments and then prompts you for a Course ID to view specific assignments.

Input:

Enter the Course ID you want to look at: 12345

Output:

--- Assignments for Course 12345 ---

ID: 67890 | Name: 09.02 - Mini-Lab Canvas Fun

ID: 67891 | Name: 10.01 - Final Project Checkpoint 2

Submitting a Repository URL
You can submit your public GitHub repository URL directly through the CLI.

Input:

Enter the Assignment ID you want to submit to: 67890

Enter your public URL: https://github.com/username/canvas-bot

Submit to assignment 67890? (y/n): y

Output:

✅ SUCCESS! Your GitHub URL has been submitted! Enjoy the bonus points!

API Endpoints Used
GET /api/v1/courses : Lists active courses where the user is enrolled as a student.

GET /api/v1/courses/:id/assignments : Retrieves all assignments for a specific course.

POST /api/v1/courses/:id/assignments/:id/submissions : Submits a website URL to a specific assignment.

Reflection
What I Learned
Through this project, I gained hands-on experience with Token-Based Authentication and the importance of managing secrets using .env files and .gitignore. I learned how to handle REST API pagination by following the Link header, ensuring that the CLI tool retrieves all available data even when Canvas limits the results per page. Also, I practiced transforming raw JSON payloads into user-friendly terminal outputs.

Challenges
The most significant challenge was correctly structuring the POST request for assignment submissions. Canvas expects a specific format for URL submissions (submission[url]), and it took review of the documentation to ensure the payload was parsed correctly by the server. Handling network errors and invalid tokens gracefully was also a priority to prevent the application from crashing with unhelpful stack traces.

Future Improvements
If I had more time, I would implement an Interactive Search feature to allow users to select courses from a list rather than typing IDs manually. I would also add a "Dashboard View" that aggregates all upcoming deadlines across all courses, color-coded by urgency, to provide a overview of my schedule.