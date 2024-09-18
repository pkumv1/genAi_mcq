import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.mcqgenerator import generate_evaluate_chain
from src.mcq_generator.logger import logging
import streamlit as st
from langchain.callbacks import get_openai_callback

# Loading Json File

with open('D:\\pavan_tests\\Pavan_python\\projects\\genAi_mcq\\response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)



# Creating Title for the app
st.title("MCQ App with Langchain")

# Create Form using st.form
with st.form("user_inputs"):
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF or a text file")

    # Input Fields
    mcq_count = st.number_input("No. of MCQ's required", min_value=3, max_value=15)

    # Input Subjects
    subject = st.text_input("What would be the subject", max_chars=25)

    # Quiz tone
    tone = st.text_input("What would be difficulty level", max_chars=25, placeholder="Simple")

    # Add Button
    button = st.form_submit_button("Create MCQ's")

    # Check if button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading"):
            try:
                text = read_file(uploaded_file)
                # Count Tokens and API
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )

                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")

                if response is not None:
                    # Extract quiz data from response
                    quiz = response.get('quiz', None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Display review in text box
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                    else:
                        st.error("Quiz data not found in the response")
                else:
                    st.error("No response received from the chain")

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred")