from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy

from arthub_w2v import western_data
from arthub_w2v import twitter
from arthub_w2v import Cos_Sim
from arthub_w2v import test2_img
# from arthub_w2v import western_noun_adj
from time import ctime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ExhbnRec.db'
app.config['SECRET_KEY'] = "dubu"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    # return render_template('index.html')
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


@app.route('/detail')  # Exhibition Detail
def detail():
    return render_template('detail.html', active='detail')


@app.route('/aboutUs')  # about Us
def aboutUs():
    return render_template('aboutUs.html', active='aboutUs')


@app.route('/elements')  # Common Elements
def elements():
    return render_template('elements.html', active='elements')


if __name__ == '__main__':
    app.run()

