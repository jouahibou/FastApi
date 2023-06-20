import requests

# Point de terminaison pour vérifier que l'API est en ligne
# OK
res = requests.get("http://localhost:8000/")
assert res.status_code == 200



# Point de terminaison pour retourner des questions
# Cela ne marche vraiment pas pouvez-vous m'orienter 


res = requests.get("http://localhost:8000/question?use=Test de positionnement&subjects=BDD&num_questions=5")
assert res.status_code == 200
questions = res.json()
assert len(questions) == 5

# Point de terminaison pour créer une nouvelle question
question = {
    "question": "Quel est le role du data engineer?",
    "subject": "data engineer",
    "responses": [
        {"text": "faire des ETL", "is_correct": True},
        {"text": "faire des sites web", "is_correct": False},
        {"text": "administrer des serveurs ", "is_correct": False},
        {"text": "rien faire ", "is_correct": False}
    ]
}
headers = {
    "Content-Type": "application/json"
}
# Cela ne marche vraiment pas aussi pouvez-vous m'orienter

res = requests.post("http://localhost:8000/questions", json=question, auth=("admin", "4dm1N"))
assert res.status_code == 200

# Point de terminaison pour vérifier l'authentification
# OK 
res = requests.get("http://localhost:8000/auth", auth=("clementine", "mandarine"))
assert res.status_code == 200
res = requests.get("http://localhost:8000/auth", auth=("clementine", "mandarine"))
assert res.status_code == 200