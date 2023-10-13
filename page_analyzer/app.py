from flask import (Flask, flash, render_template, request,
                   redirect, url_for, get_flashed_messages,
                   make_response, session, abort, g)


# конфигурация
SECRET_KEY = '13@2L8%1FRkrF57vcdv54###$@!$$$##'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
menu = ["Анализатор страниц", "Caйты"]

@app.route('/')
def index():
    return render_template('index.html',
                           menu=menu)



if __name__ == '__main__':
    app.run(debug=True)
