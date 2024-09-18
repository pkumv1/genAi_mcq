import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv

from src.mcq_generator.logger import logging
from src.mcq_generator.utils import read_file,get_table_data

#langchain Packages
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.chains import LLMChain


#loading environment variables

load_dotenv()

key = os.getenv("OPEN_API_KEY")

llm = ChatOpenAI(
    openai_api_key= key,model_name="gpt-3.5-turbo"
)

TEMPLATE = """
text:{text}
you are an expert MCQ maker. Given the above text, it is your job to \
create quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure that the questions are not repeated and check all the questions to be conforming the text as well.
make sure to format your responses like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} of MCQs
{response_json}
"""

Quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE,
)


quiz_chain=LLMChain(llm=llm,prompt=Quiz_generation_prompt, output_key="quiz", verbose = True)

TEMPLATE2 = """

you are an expert in English grammer and writing. Given a Multiple Choice Quiz for {subject} students. \
You need to evaluate the complexity of the question and provide a complete analysis of the quiz. Use only max of 50 words for the complexity evaluation.
if the Quiz is not as per the coginitive and the analytical abilities of the students,\
update the quiz questions and change the tome to suit the students abilities.
Quiz_MCQ's:
{quiz} 

Check from the english Grammer Expert and writer of the above quiz
"""


quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2,
)


review_chain = LLMChain(
    llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True
)


generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True,
)