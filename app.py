import streamlit as st
from PIL import Image
import pandas as pd
import os
import datetime
import base64

# Set page title and favicon
st.set_page_config(page_title="HappyMe", page_icon=":smiley:")

@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    [data-testid="stHeader"]{
        background-color: rgba(0 ,0 ,0 ,0);
     }
    [data-testid="stToolbar"]{
        right: 2rem;
    }
    [data-testid="stSidebar"]{
        background-position: center;
        background-image: linear-gradient(to right, rgba(182, 182, 241, 1), rgba(241, 182, 182, 1));
     }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)

#set_png_as_page_bg('background.png')
# Header
st.markdown("<h1 style='text-align: center;'>HappyMe</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Your digital companion for a healthier digital lifestyle.</h3>", unsafe_allow_html=True)

# Add separator
st.markdown("---")

# Add space
st.markdown("<br>", unsafe_allow_html=True)
# Load external CSS
def load_css(file_path):
    with open(file_path, 'r') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Load external CSS file
load_css('styles.css')

# Smiley face logo (using a local image file)
smiley_image_path = "logo.png"  # Replace with the actual path to your smiley face image
smiley_image = Image.open(smiley_image_path)

# Create an empty DataFrame for profiles
profiles_file = 'profiles.csv'
if os.path.exists(profiles_file):
    profiles = pd.read_csv(profiles_file)
else:
    profiles = pd.DataFrame(columns=["Name", "Gender", "Age"])

# Sidebar buttons
selected_page = st.sidebar.radio("Navigation", ["Profile", "Dashboard", "History"])

# Profile page
if selected_page == "Profile":
    st.subheader("Profile Customization")
    user_name = st.text_input("Enter Your Name", key="name")
    user_birthday = st.date_input("Enter Your Birthday", key="birthday",min_value=pd.to_datetime("1960-01-01"),max_value=pd.to_datetime("today")
                                  , format="YYYY-MM-DD")
    user_picture = st.file_uploader("Upload Your Profile Picture", type=["jpg", "jpeg", "png"])

    if user_birthday is not None:
        formatted_birthday = user_birthday.strftime('%Y-%m-%d')
        st.write(f"Birthday: {formatted_birthday}")
         
    # Display user's name
    st.title(f"Hello, {user_name}!")

    # Display user's profile picture if uploaded
    if user_picture is not None:
        st.image(user_picture, caption="Your Profile Picture", use_column_width=True)

    # Additional user input fields or functionalities can be added here

    # Save the user's data to a DataFrame or database
    if st.button("Save Profile"):
        # Assuming you have a DataFrame called 'user_data'
        user_data = pd.DataFrame({"Name": [user_name],"Birthday": [formatted_birthday]})

        # Additional data fields can be added here

        # Save the data to a CSV file or database
        user_data.to_csv("user_data.csv", index=False)
        st.success("Profile saved successfully!")

# Dashboard page
elif selected_page == "Dashboard":
    with st.form(key='my_form'):
        user_name = st.text_input("Enter Your Name")
        user_age = st.number_input("Enter Your Age", min_value=1, max_value=120)
        user_gender = st.selectbox("Select Your Gender", ["Male", "Female"])

        # Every form must have a submit button.
        submitted = st.form_submit_button("Save Profile")

    # Update profiles DataFrame and save to CSV
    if submitted:
        if user_name and user_gender and user_age:
            new_profile = pd.DataFrame({"Name": [user_name], "Gender": [user_gender], "Age": [user_age]})
            profiles = pd.concat([profiles, new_profile], ignore_index=True)
            # Save the profiles to a CSV file
            profiles.to_csv(profiles_file, index=False)
            st.success("Profile created/updated successfully!")
        else:
            st.warning("Please fill in all the required information.")
    st.subheader("Dashboard")
    with st.form(key='my_form1'):
        screen_time = st.number_input("Enter Your Screen Time (in hours per day)", min_value=0, max_value=24, value=0)
        submit_button = st.form_submit_button(label='Check')
        advice = ""  # Initialize advice variable
        risk = ""  # Initialize risk variable
        if submit_button:
            # Generate advice based on screen time
            if screen_time > 6:
                advice = "High screen time! Consider taking breaks and reducing screen time for better well-being."
                st.warning(advice)
            else:
                advice = "Good job on managing screen time! Remember to take breaks for eye health."
                st.success(advice)

            # Assess risk of depression based on screen time
            if screen_time > 8:
                risk = "High risk of depression! Please consider reducing screen time and seeking professional advice."
                st.error(risk)
            else:
                risk = "Low risk of depression. Keep up the good habits."
                st.info(risk)

            # Get current date
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")

            # Update profiles DataFrame and save to CSV
            new_profile = pd.DataFrame({"Name": [user_name], "Gender": [user_gender], "Age": [user_age], "Screen Time": [screen_time], "Advice": [advice], "Risk": [risk], "Date": [current_date]})
            profiles = pd.concat([profiles, new_profile], ignore_index=True)
            profiles.to_csv(profiles_file, index=False)

# History page
elif selected_page == "History":
    st.subheader("History")
    # Load external data from the CSV file
    external_data = pd.read_csv("profiles.csv")

    # Display the table with specific columns
    st.table(external_data[['Date', 'Advice', 'Risk']])

# Footer
st.markdown("---")
st.write("HappyMe - Your Digital Well-being Companion")

# Privacy statement
st.markdown("Privacy: HappyMe securely stores user data in compliance with relevant laws.")
