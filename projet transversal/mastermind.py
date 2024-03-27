import RPi.GPIO as GPIO
import random
from flask import Flask, render_template, request
import time

app = Flask(__name__)

led = {'rouge1': 17, 'vert1': 18, 'bleu1': 27,  # LED 1
            'rouge2': 22, 'vert2': 23, 'bleu2': 24,  # LED 2
            'rouge3': 5, 'vert3': 6, 'bleu3': 12,   # LED 3
            'rouge4': 13, 'vert4': 19, 'bleu4': 26} # LED 4

colors = ['rouge', 'vert', 'bleu', 'jaune', 'orange', 'violet']  

GPIO.setmode(GPIO.BCM)
for pin in led.values():
    GPIO.setup(pin, GPIO.OUT)

def code_couleur():
    return [random.choice(colors) for _ in range(4)]

def resultat(choix, code):
    correctPos = sum(choix[i] == code[i] for i in range(len(choix)))
    correctCol = sum(min(choix.count(c), code.count(c)) for c in set(colors)) - correctPos
    return correctPos, correctCol

def leds(colors):
    for pin in led.values():
        GPIO.output(pin, GPIO.LOW)  

    for i, color in enumerate(colors):
        rouge_pin = led[f"rouge{i+1}"]
        vert_pin = led[f"vert{i+1}"]
        bleu_pin = led[f"bleu{i+1}"]
        GPIO.output(rouge_pin, GPIO.LOW)
        GPIO.output(vert_pin, GPIO.LOW)
        GPIO.output(bleu_pin, GPIO.LOW)
        
        if 'rouge' in color:
            GPIO.output(rouge_pin, GPIO.HIGH)
        if 'vert' in color:
            GPIO.output(vert_pin, GPIO.HIGH)
        if 'bleu' in color:
            GPIO.output(bleu_pin, GPIO.HIGH)
        if 'jaune' in color:
            GPIO.output(rouge_pin, GPIO.HIGH)
            GPIO.output(vert_pin, GPIO.HIGH)
        if 'orange' in color:
            GPIO.output(rouge_pin, GPIO.HIGH)
            GPIO.output(vert_pin, GPIO.HIGH)
        if 'violet' in color:
            GPIO.output(rouge_pin, GPIO.HIGH)
            GPIO.output(bleu_pin, GPIO.HIGH)


@app.route('/', methods=['GET', 'POST'])
def mastermind():
    if request.method == 'POST':
        choix = [request.form['color{}'.format(i)] for i in range(1, 5)]
        correctPos, correctCol = resultat(choix, code)
        if correctPos == 4:
            return render_template('win.html', code=code)
        else:
            leds(choix)  
            time.sleep(2)  
            return render_template('mastermind.html', choix=choix, colors=colors, 
                                   correctPos=correctPos, 
                                   correctCol=correctCol)
    else:
        return render_template('mastermind.html', choix=[], colors=colors)

@app.route('/restart')
def restart():
    global code
    code = code_couleur()
    return render_template('mastermind.html', choix=[], colors=colors)

if __name__ == '__main__':
    code = code_couleur()
    app.run(debug=True, host='0.0.0.0', port=5000)
