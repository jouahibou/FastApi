import pandas as pd
from fastapi import FastAPI,HTTPException,Depends
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from typing import List
from pydantic import BaseModel

df = pd.read_csv("questions.csv")

class Response(BaseModel):
    text:str
    is_correct:bool
    
class Question(BaseModel):
    question : str
    subject : str
    Response : List[Response]  
    
app = FastAPI()
security = HTTPBasic()

@app.get("/", name ="Home")
def read_root():
    return {'Home':'Bienvenue'}     

@app.get("/questions")
def get_questions(use:str,subjects:List[str],num_questions:int):
    filtered_df = df[(df["use"] == use) & (df["subject"].isin(subjects))]
    filtered_df = filtered_df.sample(num_questions)
    questions = [] 
    for _, row in filtered_df.iterrows():
        responses = [
            Response(text=row["responseA"], is_correct=row["correct"] == "A"),
            Response(text=row["responseB"], is_correct=row["correct"] == "B"),
            Response(text=row["responseC"], is_correct=row["correct"] == "C")
        ]
        if not pd.isna(row["responseD"]):
            responses.append(Response(text=row["responseD"], is_correct=row["correct"] == "D"))
        question = Question(question=row["question"], subject=row["subject"], responses=responses)
        questions.append(question)
    
    return questions

@app.post("/questions")
def create_question(question: Question, credentials: HTTPBasicCredentials = Depends(security)):
    # Vérifier les identifiants
    if (credentials.username != "admin" or credentials.password !="4dm1N"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Ajouter la question à la base de données
    df.loc[len(df)] = [
        question.question,
        question.subject,
        question.responses[0].is_correct and "A" or 
        question.responses[1].is_correct and "B" or 
        question.responses[2].is_correct and "C" or 
        question.responses[3].is_correct and "D",
        "custom",
        question.responses[0].text,
        question.responses[1].text,
        question.responses[2].text,
        len(question.responses) == 4 and question.responses[3].text or pd.NA
    ]
    
    return {"message": "Question created successfully"}


users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

@app.get("/auth")
def check_authentication(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username not in users or users[credentials.username] != credentials.password:
       raise HTTPException(status_code=401, detail="Unauthorized")
    
    return {"message": "Authentication succeeded"}



import subprocess

# Exécute la commande pip freeze pour obtenir la liste des modules installés
result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)

# Vérifie que la commande s'est exécutée avec succès
if result.returncode != 0:
    print(f"Error executing pip freeze command: {result.stderr}")
else:
    # Écrit la liste des modules dans le fichier requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write(result.stdout)
    
    print("requirements.txt generated successfully")