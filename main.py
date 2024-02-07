from flask import Flask, render_template, request, redirect
import json
import uuid
import random


with open('g10testmm.json', 'r', encoding='utf-8-sig') as file:
    g10testmyanmar = json.load(file)

with open('grade10english.json', 'r', encoding='utf-8-sig') as file:
    g10testenglish = json.load(file)

with open('grade10maths.json', 'r', encoding='utf-8-sig') as file:
    g10testmaths = json.load(file)

with open('g11testmyanmar.json', 'r', encoding='utf-8-sig') as file:
    g11testmyanmar = json.load(file)

with open('g11testeng.json', 'r', encoding='utf-8-sig') as file:
    g11testenglish = json.load(file)

with open('g11testmaths.json', 'r', encoding='utf-8-sig') as file:
    g11testmaths = json.load(file)

with open('g12testmyanmar.json', 'r', encoding='utf-8-sig') as file:
    g12testmyanmar = json.load(file)

with open('g12testenglish.json', 'r', encoding='utf-8-sig') as file:
    g12testenglish = json.load(file)

with open('g12testmaths.json', 'r', encoding='utf-8-sig') as file:
    g12testmaths = json.load(file)

with open('highschoolmathsquiz.json', 'r', encoding='utf-8-sig') as file:
    highschoolmathsquiz = json.load(file)

with open('middleschoolmathsquiz.json', 'r', encoding='utf-8-sig') as file:
    middleschoolmathsquiz = json.load(file)

with open('primaryschoolmathsquiz.json', 'r', encoding='utf-8-sig') as file:
    primaryschoolmathsquiz = json.load(file)


with open('generalknowledgeeng.json', 'r', encoding='utf-8-sig') as file:
    generalengschoolmathsquiz = json.load(file)


with open('generalknowledgemm.json', 'r', encoding='utf-8-sig') as file:
    generalmmschoolmathsquiz = json.load(file)


app = Flask("TMD_Entrance")


numbering_map = {
    "a": "က",
    "b": "ခ",
    "c": "ဂ",
    "myanmar": "english",
    "english": "maths",
    "maths": "result",
    "english_b": "myanmar",
    "maths_b": "english",
}

def empty_answer():
    return {
        "myanmar": {str(i): "" for i in range(1, 31)},
        "english": {str(i): "" for i in range(1, 31)},
        "maths": {str(i): "" for i in range(1, 31)}
    }

student_answers = {
    "10": empty_answer(),
    "11": empty_answer(),
    "12": empty_answer()
}

student_quiz = {
    "primary": {},
    "middle": {},
    "high": {},
    "generalmm": {},
    "generaleng": {},
}


ID = str(uuid.uuid4())


@app.route('/')
def home():
    return render_template('first.html')


@app.route('/entrance/')
def entrance():
    return render_template('entrance.html')


def create_grade_route(subject, grade):
    @app.route(f"/g{grade}test{subject}/{'<id>/' if subject != 'myanmar' else ''}", methods=['GET', 'POST'], endpoint=f"/g{grade}test{subject}/")
    def g10test_subject(id=None):
        global student_answers, ID
        if request.method == 'GET':
            if (request.path == f"/g{grade}testmyanmar/"):
                ID = str(uuid.uuid4())
                student_answers = {
                    "10": empty_answer(),
                    "11": empty_answer(),
                    "12": empty_answer()
                }
            else:
                if(request.view_args['id'] != ID):
                    return redirect(f"/g{grade}testmyanmar/")
            return render_template(f'entrance_test.html', test=eval(f"g{grade}test{subject}"), grade=grade, id=ID,
                    numbering_map=numbering_map, subject=subject, url=f"/g{grade}test{subject}/{'<id>' if subject != 'myanmar' else ''}")
        elif request.method == 'POST':
            for number, answer in request.form.items():
                student_answers[str(grade)][subject][str(number)] = answer
            # print(student_answers[str(grade)][subject])
            print(student_answers[str(grade)])
            if subject == "maths":
                return redirect(f"/result/grade{grade}")

            return redirect(f"/g{grade}test{numbering_map[subject]}/{ID}")


for grade in (10, 11, 12):
    for subject in ["myanmar", "english", "maths"]:
        create_grade_route(subject, grade)

@app.route("/result/<grade>")
def result(grade):
    global student_answers
    solutions = { f"{subject}": eval(f"g{grade[-2:]}test{subject}") for subject in ["myanmar", "english", "maths"]}
    numberOfCorrectAnswers = {"myanmar": 0, "english": 0, "maths": 0}
    for subject, questions in solutions.items():
        for question in questions:
            for number, choice in question["choices"].items():
                if student_answers[grade[-2:]][subject][str(question['no'])] == number:
                    if student_answers[grade[-2:]][subject][str(question['no'])] == question['correct_answer']:
                        numberOfCorrectAnswers[subject] += 1
    
    return render_template("result.html", grade=grade[-2:], student_answers=student_answers, numbering_map=numbering_map,
     solutions=solutions, numberOfCorrectAnswers=numberOfCorrectAnswers
     )


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        return render_template('quiz.html')
    elif request.method == 'POST':
        pass

def create_student_quiz_route(level, previous_selection):
    
    @app.route(f"/{level}schoolstudentquiz/", methods=['GET', 'POST'], endpoint=f"/{level}schoolstudentquiz/")
    def quizprimarystudent():
        if request.method == 'GET':
            questions = eval(f"{level}schoolmathsquiz")
            repeat_percentage = 30
            total_questions = len(questions)
            # selection_size = int(total_questions * (1 - repeat_percentage / 100))
            selection_size = 15

            available_questions = questions.copy()

            # Remove questions from the previous selection if provided
            if len(previous_selection[level]) != 0:
                available_questions = [q for q in available_questions if q not in previous_selection[level]]

            # Select questions randomly
            selected_questions = random.sample(available_questions, selection_size)

            # Add 10% of the previous selection to the current selection
            if len(previous_selection[level]) != 0:
                repeat_size = int(selection_size * repeat_percentage / 100)
                repeated_questions = random.sample(previous_selection[level], repeat_size)
                selected_questions.pop()
                selected_questions.pop()
                selected_questions.pop()
                selected_questions.pop()
                selected_questions.extend(repeated_questions)

            # Shuffle the final selection
            random.shuffle(selected_questions)
            if len(previous_selection['primary']) != 0:
                for d in [p['no'] for p in previous_selection['primary']]:
                    if d in [p['no'] for p in selected_questions]:
                        print(d, end=",")
                print([p['no'] for p in previous_selection['primary']])
            print([p['no'] for p in selected_questions])
            student_quiz[level] = {}
            for q in selected_questions:
                student_quiz[level][str(q['no'])] = ""
            previous_selection[level] = selected_questions
            return render_template('schoolLevelQuiz.html', level=level, questions=enumerate(selected_questions),
            url=f"/{level}schoolstudentquiz/")
        elif request.method == 'POST':
            for number, answer in request.form.items():
                student_quiz[level][number] = answer
            return redirect(f"/schoolLevelQuizResult/{level}")
    

for level in ["primary", "middle", "high", "generalmm", "generaleng"]:
    previous_selection = {
        "primary": [],
        "middle": [],
        "high": [],
        "generalmm": [],
        "generaleng": [],
    }
    create_student_quiz_route(level, previous_selection)


@app.route("/schoolLevelQuizResult/<level>")
def resultSchoolLevelQuiz(level):
    global student_quiz
    questions = eval(f"{level}schoolmathsquiz")
    correct_answers = {str(q['no']): q['correct_answer'] for q in questions}
    numberOfCorrectAnswers = 0
    Questions = {str(q['no']): q for q in questions}
    random_questions = [Questions[number] for number in student_quiz[level].keys()]

    for number, answer in student_quiz[level].items():
        if(correct_answers[number] == answer):
            numberOfCorrectAnswers += 1
    return render_template("resultSchoolLevelQuiz.html", level=level, answers=student_quiz[level], 
    numberOfCorrectAnswers=numberOfCorrectAnswers, questions=enumerate(random_questions))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
