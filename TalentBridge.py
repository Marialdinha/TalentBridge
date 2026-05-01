# Application name: TalentBridge
# Creator: Marialda Cabral
# This application facilitates the interview process 


# ==========================================
# IMPORTS & SETUP
# ==========================================
import streamlit as st
import pandas as pd
import os


# Define Questions Excel file path
QUESTIONS_FILE = 'interview_questions.xlsx'
# Define Questions Excel file columns
QUESTIONS_COLUMNS = ["QuestionId", "Question"]

# Define Responses Excel file path
RESPONSES_FILE = 'interview_responses.xlsx'
# Define Responses Excel file columns
RESPONSES_COLUMNS = ["UserId", "QuestionId", "Answer"]

# Define Users Excel file path
USERS_FILE = 'Users.xlsx'
# Define Users Excel file columns
USERS_COLUMNS = ["UserId", "First Name", "Last Name", "Role"]

# Define Assigned Questions Excel file path
ASSIGNED_QUESTIONS_FILE = 'assigned_questions.xlsx'
# Define Assigned Questions Excel file columns
ASSIGNED_QUESTIONS_COLUMNS = ["CandidateId", "QuestionId"]


# ==========================================
# STATE MANAGEMENT
# ==========================================
#-----
# Initializing session state variables
#-----

# We use session state to remember where the user is in the process
def initializing_session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = {}

#-----
# Clearing session state variables
#-----

# We use session state to remember where the user is in the process
def clear_session():
        st.session_state.logged_in = False
        st.session_state.current_user = {}

# ==========================================
# DATA HANDLING 
# ==========================================
#-----
# Retriving data from User file
#-----
def load_users():
    
    # Loads the users file. Creates it if it doesn't exist.
    if not os.path.exists(USERS_FILE):
        # Create an empty DataFrame with the required columns
        df = pd.DataFrame(columns=USERS_COLUMNS)
        df.to_excel(USERS_FILE, index=False)
        return df
    return pd.read_excel(USERS_FILE)

#-----
# Adding user to User file
#-----
def add_user(df,first_name, last_name, role):
    
    # Generate a simple UserId 
    if df.empty:
        new_user_id = 1
    else:
        new_user_id = df['UserId'].max() + 1 
    
    new_user = pd.DataFrame([{
        'UserId': new_user_id,
        'First Name': first_name, 
        'Last Name': last_name, 
        'Role': role
    }])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(USERS_FILE, index=False)

#-----
# Retrieving data from Questions file
#-----
def load_questions():
    # Loads the questions file. Creates it if it doesn't exist.
    if not os.path.exists(QUESTIONS_FILE):
        df = pd.DataFrame(columns=QUESTIONS_COLUMNS)
        df.to_excel(QUESTIONS_FILE, index=False)
        return df
    return pd.read_excel(QUESTIONS_FILE)

#-----
# Adding question to Questions file
#-----
def add_question(df, question_text):
    # Generate a simple QuestionId
    new_question_id = len(df) + 1 
    
    new_question = pd.DataFrame([{
        'QuestionId': new_question_id,
        'Question': question_text
    }])
    df = pd.concat([df, new_question], ignore_index=True)
    df.to_excel(QUESTIONS_FILE, index=False)
    return df

#-----
# Retrieving data from Responses file
#-----
def load_responses():
    # Loads the responses file. Creates it if it doesn't exist.
    if not os.path.exists(RESPONSES_FILE):
        df = pd.DataFrame(columns=RESPONSES_COLUMNS)
        df.to_excel(RESPONSES_FILE, index=False)
        return df
    return pd.read_excel(RESPONSES_FILE)

#-----
# Saving Candidate Responses
#-----
def save_responses(user_id, answers_dict):
    df = load_responses()
    
    # Remove existing responses for this user so we can update them cleanly
    df = df[df['UserId'] != user_id]
    
    # Create new rows for the answers
    new_rows = []
    for q_id, answer in answers_dict.items():
        if answer.strip(): # Only save if the candidate actually typed something
            new_rows.append({
                'UserId': user_id,
                'QuestionId': q_id,
                'Answer': answer.strip()
            })
            
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_df], ignore_index=True)
        
    df.to_excel(RESPONSES_FILE, index=False)

#-----
# Retrieving data from Assigned Questions file
#-----
def load_assigned_questions():
    # Loads the assigned questions file. Creates it if it doesn't exist.
    if not os.path.exists(ASSIGNED_QUESTIONS_FILE):
        df = pd.DataFrame(columns=ASSIGNED_QUESTIONS_COLUMNS)
        df.to_excel(ASSIGNED_QUESTIONS_FILE, index=False)
        return df
    return pd.read_excel(ASSIGNED_QUESTIONS_FILE)

#-----
# Assigning questions to a candidate
#-----
def assign_questions(candidate_id, question_ids):
    df = load_assigned_questions()
    
    # Remove existing assignments for this candidate to replace with the new selection
    df = df[df['CandidateId'] != candidate_id]
    
    # Create new assignments
    new_rows = [{'CandidateId': candidate_id, 'QuestionId': q_id} for q_id in question_ids]
    
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_df], ignore_index=True)
        
    df.to_excel(ASSIGNED_QUESTIONS_FILE, index=False)

    
# ==========================================
# FUNCTIONS
# ==========================================
#-----
# Login Page
#-----
def Login_page(user_df):

    # Centering Title and slogan
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>TalentBridge</h1>
            <p style="font-size: 18px; color: gray;"><i>Where talent meets opportunity</i></p>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )

    # Create 3 columns. The middle one is twice as wide as the side ones.
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # Show the banner in the middle column
    with col2:
        # The image will now only fill the middle column, keeping it centered and smaller!
        st.image("TalentBridge.png", use_container_width=True)

    # Request user information 
    st.write("Please enter your details to continue.")
    fname_input = st.text_input("First Name").strip()

    # Only show subsequent inputs if te previous ones are filled out
    if fname_input:
        lname_input = st.text_input("Last Name").strip()

        # Check if the user already exists (case-insensitive)
        if lname_input:
            user_record = user_df[(user_df['First Name'].str.strip().str.lower() == fname_input.strip().lower()) & 
            (user_df['Last Name'].str.strip().str.lower() == lname_input.strip().lower())]

            # If user exists
            if not user_record.empty:
                st.success("Login successful!")
                # Update session state
                st.session_state.logged_in = True
                st.session_state.current_user = user_record.iloc[0].to_dict()
                st.rerun() # Refresh the app to show the main dashboard
            # Does Not Exists
            else:
                role_input = st.selectbox(
                "Select your role", 
                ["Manager", "Interviewer", "Candidate"],
                index=None,
                placeholder="Select a role...")
                if role_input:
                    if st.button("Save User"):
                        # Save data in excel spreadsheet by calling our updated function
                        add_user(user_df, fname_input, lname_input, role_input)
                        st.rerun() # Refresh the app to show the main dashboard
      
#-----
# Dashboard Page
#-----
# Dashboard Page (What users sees after logging in)
def dashboard_page():
    st.title(f"Welcome to TalentBridge, {st.session_state.current_user['First Name']}!")
    st.write(f"**Role:** {st.session_state.current_user['Role']}")
    
    st.markdown("---")
    
    # Selects page depending on role
    if st.session_state.current_user['Role'].lower() == "manager":
        manager_page()
    elif st.session_state.current_user['Role'].lower() =="interviewer":
        interviewer_page()
    else:
        candidate_page()

    if st.button("Logout"):
        clear_session()
        st.rerun()

#-----
# Manager Page
#-----
# Manager Page (What managers sees after logging in)
def manager_page():
    st.subheader("👨‍💼 Manager Dashboard")
    
    # Let the manager choose what they want to see
    manager_action = st.selectbox(
    "What would you like to do?",
    ["Create Questions", "View Candidate Answers"],
    index=None,
    placeholder="Select an action..."
    )
    
    st.markdown("---")

    #  Create Questons
    if manager_action == "Create Questions":
        add_question_page()
    #  View Candidate Answers
    elif manager_action == "View Candidate Answers":
        view_candidate_answers_page()
        
    
#-----
# Add questions Page
#-----
# Managers use this page to add questions to file
def add_question_page():
    st.subheader("📝 Manage Interview Questions")
    
    # Load existing questions
    questions_df = load_questions()
    
    # Form to add a new question
    with st.form("add_question_form", clear_on_submit=True):
        st.write("### Add a New Question")
        new_question_text = st.text_area("Enter the interview question here:", height=100)
        
        submitted = st.form_submit_button("Save Question")
        
        if submitted:
            if not new_question_text.strip():
                st.error("Question cannot be empty. Please enter a valid question.")
            else:
                # Add the question and get the updated dataframe back
                questions_df = add_question(questions_df, new_question_text.strip())
                st.success("Question added successfully!")
    
    # Display existing questions
    st.write("### Current Question Bank")
    if not questions_df.empty:
        st.dataframe(questions_df, use_container_width=True, hide_index=True)
    else:
        st.info("The question bank is currently empty. Add a question above to get started.")
    

#-----
# View Candidate Answers Page
#-----
# Managers use this page to review submitted answers
def view_candidate_answers_page():
    st.subheader("📄 Candidate Responses")
    
    # Load required data
    users_df = load_users()
    questions_df = load_questions()
    responses_df = load_responses()
    
    # Filter users to only show Candidates
    candidates_df = users_df[users_df['Role'].str.lower() == 'candidate']
    
    if candidates_df.empty:
        st.info("No candidates found in the system yet.")
        return
        
    # Create a dictionary mapping UserId to Candidate Name for the dropdown     
    candidate_dict = {}
    for _, row in candidates_df.iterrows():
        candidate_dict[row['UserId']] = f"{row['First Name']} {row['Last Name']}"
        
    # Let the manager select a candidate
    selected_candidate_id = st.selectbox(
        "Select a Candidate to review:",
        options=list(candidate_dict.keys()),
        format_func=lambda x: candidate_dict[x], # Shows the name instead of the ID
        index=None,
        placeholder="Choose a candidate..."
    )
    
    # Only show answers if a candidate is actually selected
    if selected_candidate_id is not None:
        st.write(f"### Responses for {candidate_dict[selected_candidate_id]}")
        
        # Filter responses for this specific candidate
        candidate_responses = responses_df[responses_df['UserId'] == selected_candidate_id]
        
        if candidate_responses.empty:
            st.warning("This candidate has not answered any questions yet.")
        else:
            # Merge responses with questions so we can display the actual question text
            merged_df = pd.merge(candidate_responses, questions_df, on="QuestionId", how="left")
            
            # Display each Question and Answer
            for index, row in merged_df.iterrows():
                with st.container():
                    st.markdown(f"**Question {index + 1}:** {row['Question']}")
                    st.info(f"**Answer:** {row['Answer']}")

#-----
# Interviewer Page
#-----
# Interviewer Page (What interviewers sees after logging in)
def interviewer_page():
    st.subheader("🗣️ Interviewer Dashboard")
    
     # Let the interviewer choose what they want to see
    interviewer_action = st.selectbox(
    "What would you like to do?",
    ["Assign Questions", "View Candidate Answers"],
    index=None,
    placeholder="Select an action..."
    )
    
    st.markdown("---")

    #  Assign Questons
    if interviewer_action == "Assign Questions":
        assign_questions_page()
    #  View Candidate Answers
    elif interviewer_action == "View Candidate Answers":
        view_candidate_answers_page()

  
                
#-----
# Assign Questions Page
#-----
# Assign Questions Page (Interviewers assign which questions they want candidate to asnwer)
def assign_questions_page():

    st.write("Assign questions to candidates for their interview.")
    
    # Load users and filter for candidates
    users_df = load_users()
    candidates_df = users_df[users_df['Role'].str.lower() == 'candidate']
    
    if candidates_df.empty:
        st.info("No candidates available in the system.")
        return
        
    # Create a dictionary mapping UserId to Candidate Name
    candidate_dict = {}
    for _, row in candidates_df.iterrows():
        candidate_dict[row['UserId']] = f"{row['First Name']} {row['Last Name']}"
        
    # Step 1: Select a candidate
    selected_candidate_id = st.selectbox(
        "Select a Candidate:",
        options=list(candidate_dict.keys()),
        format_func=lambda x: candidate_dict[x],
        index=None,
        placeholder="Choose a candidate..."
    )
    
    # Step 2: Choose questions for the selected candidate
    if selected_candidate_id is not None:
        questions_df = load_questions()
        
        if questions_df.empty:
            st.warning("No questions available in the question bank. Please ask a manager to add some.")
            return
            
        # Load currently assigned questions to pre-select them
        assigned_df = load_assigned_questions()
        current_assignments = assigned_df[assigned_df['CandidateId'] == selected_candidate_id]['QuestionId'].tolist()
        
        # Create a dictionary mapping QuestionId to Question Text
        question_dict = {row['QuestionId']: row['Question'] for _, row in questions_df.iterrows()}
        
        with st.form("assign_questions_form"):
            st.write(f"### Select Questions for {candidate_dict[selected_candidate_id]}")
            
            # Multiselect for questions
            selected_question_ids = st.multiselect(
                "Available Questions:",
                options=list(question_dict.keys()),
                default=[q_id for q_id in current_assignments if q_id in question_dict],
                format_func=lambda x: question_dict[x]
            )
            
            submitted = st.form_submit_button("Save Assignments")
            
            if submitted:
                if len(selected_question_ids) == 0:
                    st.warning("Please select at least one question before saving.")
                else:
                    assign_questions(selected_candidate_id, selected_question_ids)
                    st.success(f"Questions successfully assigned to {candidate_dict[selected_candidate_id]}!")


#-----
# Candidate Page
#-----
# Candidate Page (What candidates sees after logging in)
def candidate_page():

    st.subheader("📝 My Interview Questions")
    
    # Get the current logged in candidate's ID
    current_user_id = st.session_state.current_user['UserId']
    
    # Load necessary data
    assigned_df = load_assigned_questions()
    questions_df = load_questions()
    responses_df = load_responses()
    
    # Find questions assigned to this specific candidate
    my_assigned_questions = assigned_df[assigned_df['CandidateId'] == current_user_id]
    
    if my_assigned_questions.empty:
        st.info("You currently have no interview questions assigned. Please check back later.")
        return
        
    # Get the actual question text for the assigned IDs
    assigned_q_ids = my_assigned_questions['QuestionId'].tolist()
    my_questions = questions_df[questions_df['QuestionId'].isin(assigned_q_ids)]
    
    # Get previous answers (if the candidate already started answering)
    my_previous_responses = responses_df[responses_df['UserId'] == current_user_id]
    prev_answers_dict = {}
    if not my_previous_responses.empty:
        prev_answers_dict = dict(zip(my_previous_responses['QuestionId'], my_previous_responses['Answer']))
        
    st.write("Please answer the following questions. Make sure to click **'Submit All Answers'** at the bottom when you are finished.")
    
    # Create a form so the page doesn't refresh after every single keystroke
    with st.form("candidate_answers_form"):
        answers = {}
        
        # Loop through each assigned question and display a text area
        for index, row in my_questions.iterrows():
            q_id = row['QuestionId']
            q_text = row['Question']
            
            # Pre-fill with their previous answer if it exists
            default_ans = prev_answers_dict.get(q_id, "")
            
            st.markdown(f"**Question:** {q_text}")
            
            # We use a unique key for each text area based on the QuestionId
            answers[q_id] = st.text_area(
                f"Your Answer for Question {q_id}", 
                value=default_ans, 
                key=f"q_{q_id}", 
                label_visibility="collapsed",
                height=150
            )
            st.markdown("---")
            
        # The submit button for the entire form
        submitted = st.form_submit_button("Submit All Answers", type="primary")
        
        if submitted:
            # Check if all values in the dictionary are empty strings (or just spaces)
            if all(answer.strip() == "" for answer in answers.values()):
                st.warning("In order to save, at least one question needs to be responded.")
            else:
                save_responses(current_user_id, answers)
                st.success("Your answers have been successfully submitted! Thank you.")


# ==========================================
# MAIN APP EXECUTION
# ==========================================

# Initializing session state variables 
initializing_session()

# Routing: Show Login page if not logged in, otherwise show Dashboard
if not st.session_state.logged_in:
    # Retrieving users
    df = load_users()
    Login_page(df)
else:
    dashboard_page()
















    
