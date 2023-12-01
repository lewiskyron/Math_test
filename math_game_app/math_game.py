from flask import Flask, render_template, session, request, redirect, url_for
import random
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace this with a secure secret key


def generate_question():
    """Function to generate a random math question"""
    operations = ["+", "-", "*", "/"]
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(operations)
    question = f"{num1} {operation} {num2}"
    answer = round(eval(question), 2)  # Round to 2 decimal places for division
    return question, answer


@app.route("/")
def home():
    """Route to serve the home page"""
    session.clear()  # Clear any existing session data
    return render_template("home.html")


@app.route("/start_game", methods=["POST"])
def start_game():
    """Route to initialize the game and redirect to the game page"""
    session["user"] = 1
    session["round"] = 1
    session["start_time"] = time.time()
    session["questions"] = [generate_question() for _ in range(10)]
    session["current_question"] = 0
    return redirect(url_for("play_game"))


@app.route("/play_game")
def play_game():
    """Route to display the current math question"""
    if "questions" not in session or session["current_question"] >= 10:
        return redirect(url_for("end_round"))

    question, _ = session["questions"][session["current_question"]]
    return render_template("game.html", question=question, user=session["user"])


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    """Route to handle the submission of answers"""
    _, answer = session["questions"][session["current_question"]]
    user_answer = request.form["answer"]
    session["current_question"] += 1

    # Here you can add logic to check if the answer is correct
    # For now, it just proceeds to the next question

    return redirect(url_for("play_game"))


@app.route("/end_round")
def end_round():
    """Route to handle the end of a round"""
    elapsed_time = time.time() - session["start_time"]
    if session["user"] == 1:
        session["user1_time"] = elapsed_time
        session["user"] = 2
        session["start_time"] = time.time()
        session["current_question"] = 0
        return render_template("wait_for_user2.html")
    else:
        session["user2_time"] = elapsed_time
        winner = "User 1" if session["user1_time"] < session["user2_time"] else "User 2"
        return render_template(
            "results.html",
            winner=winner,
            user1_time=session["user1_time"],
            user2_time=session["user2_time"],
        )


if __name__ == "__main__":
    app.run(debug=True)
