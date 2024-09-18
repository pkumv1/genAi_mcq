import os
import json
import PyPDF2
import traceback



def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=pyPDF2.pdfFilereader(file)
            text = ""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("error reading the pdf file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported Files, please upload .txt of .pdf file only"
        )
        
        
def get_table_data(quiz_str):
    try:
        #converting quiz from string to dictionary
        quiz.dict=json.loads(quiz_str)
        quiz_table_data=[]
        
        
        # iterate over quiz dictionary and extract data
        
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options = " || ".join(
                [
                    f"{option} -. {option_value}" for option,Option_value in value["options"].items()
                ]
            )
            correct= value["correct"]
            quiz_table_data.append({"MCQ": mcq,"Choices":options,"Correct":correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e._traceback__)
        return False