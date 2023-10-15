import os
from dotenv import load_dotenv
from flask import (Flask, flash, render_template, request,
                   redirect, url_for, get_flashed_messages,
                   make_response, session, abort, g)


# конфигурация
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True


app = Flask(__name__)
app.config.from_object(__name__)
menu = ["Анализатор страниц", "Caйты"]

@app.route('/')
def index():
    return render_template('index.html',
                           menu=menu)


def main():
    app.run(debug=True)

print(SECRET_KEY)
# if __name__ == '__main__':
#     main()
