from flask import Flask, render_template, request, redirect, url_for
from db_team import Base, Team
from db_arthub import Base, Arthub
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from input import art_input
import pandas as pd
import input_book
import matplotlib.pyplot as plt
import io
import base64

from arthub_d2v import western_data
from arthub_d2v import lda_sim
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ExhbnRec.db'
app.config['SECRET_KEY'] = "dubu"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

conn = sqlite3.connect("ExhbnRec.db")
cur = conn.cursor()
data_final = pd.read_sql_query('SELECT * FROM arthub_info', conn)

best_seller = input_book.get_bestseller()
all_book = input_book.input_book()
book_name_list = all_book.name.tolist()


@app.route('/index_art')
def index_art():
    return render_template('index.html', famous_paint=art_input(), active='index_art')


@app.route('/', methods=['GET'])
def index_book():
    if request.method == 'GET':

        book_name = request.args.get('book_name')  # 책 제목을 받음
        try:
            if book_name :
                if book_name not in book_name_list:
                    message = '다음 도서를 검색할 수 없습니다:{}'.format(book_name)

                    return render_template('index_book.html', best_seller=best_seller,
                                           book_name_list=book_name_list, active='index_book',
                                           message=message)

                book_author = all_book[all_book['name'] == book_name].author.values[0]
                book_content = all_book[all_book['name'] == book_name].text.values[0]
                book_image = all_book[all_book['name'] == book_name].image.values[0]

                plot_url=input_book.word_cloud(book_name)

                return render_template('index_book.html', best_seller=best_seller, book_name_list=book_name_list,
                                       book_name=book_name, book_author=book_author, book_content=book_content,
                                       book_image=book_image, plot_url=plot_url, active='index_book')

            else:
                return render_template('index_book.html', best_seller=best_seller, book_name_list=book_name_list, active='index_book')

        except Exception as e:
            print(e)


@app.route('/exhbnRec', methods = ['POST','GET']) # Exhibition Recommendation
def exhbnRec():
    test_txt_list = []

    title = ''
    try:
        title = request.form['title']
    except:
        pass

    if title != '':
        book_corpus = all_book[all_book.name == title].noun
        sims = lda_sim(book_corpus, data_final)

    elif title=='':
        result = request.form
        result_selected = []

        for key in result.keys():
            if result[key] == '1':
                result_selected.extend(key)

        if not result_selected:
            return redirect(url_for('index_art'))

        for index in result_selected:
            test_txt_list.append(western_data['noun'][int(index)])

        test_txt_list = test_txt_list[0].split(',')

        sims = lda_sim(test_txt_list, data_final)
    else:
        return render_template('index_book.html', best_seller=best_seller, book_name_list=book_name_list, active='index_book')

    simsKeys = list(sims.keys())

    q = db.session.query(Arthub).filter(Arthub.id.in_(simsKeys))
    query_as_string = str(q.statement.compile(compile_kwargs={"literal_binds": True}))
    model=db.session.execute(query_as_string).fetchall()

    simsVal = []
    sorted_sims = sorted(sims.items(), key=lambda kv: kv[1], reverse=True)
    for tpl in sorted_sims:
        simsVal.append(tpl[1])

    return render_template('exhbnRec.html', active='exhbnRec', sims=simsVal, model=model)


@app.route('/aboutUs')  # about Us
def aboutUs():
    model = db.session.query(Team).all()
    return render_template('aboutUs.html', active='aboutUs', model=model)


@app.route('/intro')  # introduce
def intro():
    return render_template('intro.html', active='intro')


@app.route('/skills')  # Common Elements
def skills():
    return render_template('skills.html', active='skills')


@app.route('/elements')  # Common Elements
def elements():
    return render_template('elements.html', active='elements')


if __name__ == '__main__':
    app.run()

