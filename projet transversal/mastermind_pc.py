import random
from flask import Flask, render_template, request

app = Flask(__name__)

colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple'] 

def generate_code():
    return [random.choice(colors) for _ in range(4)]

def check_guess(guess, code):
    correct_color_and_position = sum(a == b for a, b in zip(guess, code))
    correct_color_only = sum(min(guess.count(c), code.count(c)) for c in set(colors)) - correct_color_and_position
    return correct_color_and_position, correct_color_only

@app.route('/', methods=['GET', 'POST'])
def mastermind():
    if request.method == 'POST':
        guess = [request.form['color{}'.format(i)] for i in range(1, 5)]
        correct_color_and_position, correct_color_only = check_guess(guess, code)
        if correct_color_and_position == 4:
            return render_template('win.html', code=code)
        else:
            return render_template('mastermind.html', guess=guess, colors=colors, 
                                   correct_color_and_position=correct_color_and_position, 
                                   correct_color_only=correct_color_only)
    else:
        return render_template('mastermind.html', guess=[], colors=colors)

@app.route('/restart')
def restart():
    global code
    code = generate_code()
    return render_template('mastermind.html', guess=[], colors=colors)

if __name__ == '__main__':
    code = generate_code()
    app.run(debug=True)
