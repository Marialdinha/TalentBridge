# TalentBridge 🌉

**Creator:** Marialda Cabral  
**Description:** A Streamlit-based web application designed to streamline the interview process. TalentBridge connects managers, interviewers, and candidates in one unified, easy-to-use platform.

## 🌟 Features

TalentBridge features a role-based dashboard that adapts to the user logging in:

*   **👨‍💼 Managers**
    *   **Question Bank Management:** Create and add new interview questions to the company database.
    *   **Review Submissions:** Read through the answers submitted by candidates.
*   **🗣️ Interviewers**
    *   **Assign Questions:** Select specific questions from the question bank and assign them to individual candidates.
    *   **Review Submissions:** View candidate responses to evaluate their performance.
*   **📝 Candidates**
    *   **Asynchronous Interviews:** View questions specifically assigned to them.
    *   **Submit Answers:** Draft and submit answers to interview questions in a clean, distraction-free interface.

## 🛠️ Prerequisites

Before running the application, ensure you have Python installed on your computer. You will also need to install the required Python libraries.
(Note: openpyxl is required by Pandas to read and write Excel files).
```bash
pip install streamlit pandas openpyxl
```  


🚀 How to Run the Application

Download or clone this repository to your local machine.
Ensure you have the TalentBridge.png image file in the same directory as your script (for the login page banner).
Open your terminal or command prompt.
Navigate to the folder containing talentbridge.py.
Run the following command:
```bash
streamlit run talentbridge.py
```  

The application will automatically open in your default web browser.

📂 Project Structure & Data Storage

This application uses local Excel files as a lightweight database. You do not need to create these files manually. The application will automatically generate them in the same folder the first time you run it:

Users.xlsx: Stores user profiles (First Name, Last Name, Role).
interview_questions.xlsx: Stores the bank of questions created by Managers.
assigned_questions.xlsx: Tracks which questions have been assigned to which candidates.
interview_responses.xlsx: Stores the answers submitted by candidates.

💡 Usage Guide (First Time Setup)

Create a Manager Account: Open the app, enter your First and Last name. Since you are not in the system yet, it will prompt you to select a role. Choose Manager and click "Save User".
Add Questions: As a Manager, go to "Create Questions" and add a few sample interview questions.
Create a Candidate: Log out, then log in with a new name. Select the Candidate role.
Create an Interviewer: Log out, log in with a third name, and select Interviewer. Use this account to assign the questions you created in Step 2 to the Candidate you created in Step 3.
Test the Flow: Log back in as the Candidate to see your assigned questions and submit your answers!

🔮 Future Roadmap

Migration from Excel files to SQLite for improved concurrency and performance.
Implementation of secure password authentication.
Email notifications for candidates when questions are assigned.
