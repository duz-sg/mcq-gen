import os
import json
from flask import Response
import traceback2
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.mcqgen import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import streamlit as st

with open('D:\Code\Gen-AI\mcq-gen\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
    st.title("MCQs Creator Application with LangChain and Google Palm")
#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Uplaod a PDF or txt file")

    #Input Fields
    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=100)

    #Subject
    subject=st.text_input("Insert Subject", max_chars=200)

    # Quiz Tone
    tone=st.text_input("Complexity Level Of Questions", max_chars=30, placeholder="Hard")

    #Add Button
    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone: 
        with st.spinner("Hang on champ..."):
                try:
                   text=read_file(uploaded_file)
               #Count tokens and the cost of API call
                   Response = generate_evaluate_chain(
    {
        "text": text,
        "number": mcq_count,
        "subject": subject,
        "tone": tone,
        'response_json':RESPONSE_JSON
    }
)

                except Exception as e:
                     traceback2.print_exception(type(e), e, e.__traceback__)
                     st.error(e)

                     if isinstance(Response, dict):
                # Extract the quiz data from the response
                         quiz = Response.get("quiz", None)

                if 'quiz' is not None:
                    # Extract the table data from the quiz
                    table_data = get_table_data('quiz')

                    if table_data is not None:
                        # Convert the table data to a pandas dataframe
                        df = pd.DataFrame(table_data)

                        # Set the index of the dataframe
                        df.index = df.index + 1

                        # Display the dataframe as a table
                        st.table(df)

                        # Display the review in a text area as well
                        st.text_area(label="Review", value=Response["review"])
                    else:
                        st.error("Error in the table data")
                else:
                    st.write(Response)
            

                    