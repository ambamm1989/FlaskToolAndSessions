from crypt import methods
from distutils.log import debug
from gzip import READ
from http.client import responses
from secrets import choice
from urllib import response
from flask import flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-told"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """Choose a Survey."""
    return render_template("survey_start.html", survey = survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the responses"""

    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save survey response and goes to next question."""

    choice = request.form['answer']

    response = session[RESPONSES_KEY]
    response.append(choice)
    session[RESPONSES_KEY] = responses
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Show current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")
    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    if(len(responses) !=qid):
        flash(f"Question not valid: {qid}.")
        return redirect(f"/question/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    """Suvery done. Show finished page."""
    return render_template("completion.html")