from flask import Flask, render_template, request, redirect, url_for
from db import Base, Team
from flask_sqlalchemy import SQLAlchemy

from arthub_w2v import western_data
from arthub_w2v import twitter
from arthub_w2v import Cos_Sim
from arthub_w2v import test2_img
from time import ctime

from input_book import *
import matplotlib.pyplot as plt
import io
import base64


best_seller = get_bestseller()
all_book = input_book()
book_name_list = all_book.name.tolist()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ExhbnRec.db'
app.config['SECRET_KEY'] = "dubu"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    from input import art_input

    sample_data = art_input()

    return render_template('index.html', sample_data = sample_data, active='index')


@app.route('/exhbnRec', methods = ['POST']) # Exhibition Recommendation
def exhbnRec():
    result=request.form
    result_selected = []
    print(result)

    print('before get key: ', ctime())
    for key in result.keys():
        if result[key] == '1':
            result_selected.append(key)
    # print(result_selected)
    print('after get key: ', ctime())

    if not result_selected:
        from input import art_input
        sample_data = art_input()
        return render_template('index.html', sample_data = sample_data, active='index')

    test_txt_list = []

    print('before noun and adj: ', ctime())
    for index in result_selected:
        pos = twitter.pos(western_data['text'][int(index)])
        words = []

        for word, tag in pos:
            if tag == 'Adjective' or tag == 'Noun':
                words.append(word)
        test_txt_list += words
    # print("test txt lenth: ", len(test_txt_list))
    print('after noun and adj: ', ctime())

    print('before cos_sim: ', ctime())
    sims = Cos_Sim(test_txt_list)
    sims = sims[:12]
    print('after cos_sim: ', ctime())

    # print("Posted data : {}".format(request.form))
    return render_template('exhbnRec.html', active='exhbnRec', sims=sims, test2=test2_img)




@app.route('/index_book', methods=['GET'])
def index_book():

    try:
        if request.args.get('book_name') :
            book_name = request.args.get('book_name')  # 책 제목을 받음
            # search 기능
            print(book_name)

            # plot_url = word_cloud(book_name)

            book_author = all_book[all_book['name'] == book_name].author.values[0]
            book_content = all_book[all_book['name'] == book_name].text.values[0]
            book_image = all_book[all_book['name'] == book_name].image.values[0]

            print('입력 처리 성공 !!')

            return render_template('index_book.html', best_seller=best_seller, book_name_list=book_name_list,
                                   book_name=book_name, book_author=book_author, book_content=book_content,
                                   book_image=book_image)#, plot_url=plot_url)

        else :
            print('미입력 상태 처리 성공 !!')
            return render_template('index_book.html', best_seller=best_seller, book_name_list=book_name_list)


    except Exception as e :
        print(e)
        print('실패 ㅠㅠ')






# @app.route('/index_book', methods=['GET'])
# def index_book():
#     try:
#         # search 기능
#         book_name = request.args.get('book_name')  # 책 제목을 받음
#         print(book_name)
#
#         plot_url = word_cloud(book_name)
#
#         book_author = all_book[all_book['name'] == book_name].author.values[0]
#         book_content = all_book[all_book['name'] == book_name].text.values[0]
#         book_image = all_book[all_book['name'] == book_name].image.values[0]
#
#         return render_template('index_book.html', best_seller=best_seller, book_name_list=book_name_list,
#                                book_name=book_name, book_author=book_author, book_content=book_content,
#                                book_image=book_image, plot_url=plot_url)
#     except Exception as e:
#         print(e)
#         return render_template('index_book.html', best_seller=best_seller, book_name_list=book_name_list)



@app.route('/detail')  # Exhibition Detail
def detail():
    return render_template('detail.html', active='detail')


@app.route('/aboutUs')  # about Us
def aboutUs():
    model=db.session.query(Team).all()
    # for row in db.session.query(Team.id, Team.name,)
    print("이거야",model)

    for row in model:
        print(row)

    return render_template('aboutUs.html', active='aboutUs', model=model)


@app.route('/elements')  # Common Elements
def elements():
    return render_template('elements.html', active='elements')


if __name__ == '__main__':
    app.run()

