import pandas as pd

def input_book():
    # all_book = pd.read_csv('static/books_all.csv')
    all_book = pd.read_excel('static/books_all.xlsx')

    # del all_book['Unnamed: 0']
    # all_book.reset_index(drop=True, inplace=True)

    return all_book


def get_bestseller():
    all_book = input_book()
    ko_bestseller = all_book[all_book.genre == '한국소설'][:5]
    jp_bestseller = all_book[all_book.genre == '일본소설'][:5]
    en_bestseller = all_book[all_book.genre == '영미소설'][:5]
    etc_bestseller = all_book[all_book.genre == '기타 외국 소설'][:5]
    bestseller = pd.concat([ko_bestseller, jp_bestseller, en_bestseller, etc_bestseller])

    return bestseller.sample(20)


def word_cloud(book_name):
    # !pip install wordcloud

    import nltk
    from konlpy.corpus import kobill
    from konlpy.tag import Twitter;
    t = Twitter()
    from wordcloud import WordCloud

    import matplotlib.pyplot as plt
    import platform
    import io
    import base64
    img = io.BytesIO()


    # OS별 matplotlib 한국어 처리
    path = "static/AppleGothic.ttf" # window 사용자의 경우 path 설정 중요
    from matplotlib import font_manager, rc
    if platform.system() == 'Darwin':
        rc('font', family='AppleGothic')
    elif platform.system() == 'Windows':
        font_name = font_manager.FontProperties(fname=path).get_name()
        rc('font', family=font_name)
    else:
        print('Unknown system... sorry~~~~')

    # 워드 클라우드 만들기 시작

    files_ko = kobill.fileids()
    books_all = pd.read_csv('static/books_all.csv')

    book_name = book_name  # input으로 받음

    files_ko = kobill.fileids()

    doc_ko = books_all[books_all['name'] == book_name].iloc[0].text
    tokens_ko = t.nouns(doc_ko)

    with open('static/project_stopwords.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().split(' ')

    ko = nltk.Text(tokens_ko)
    ko = [each_word for each_word in ko if each_word not in stop_words]
    ko = nltk.Text(ko)

    data = ko.vocab().most_common(150)

    # for win : font_path='c:/Windows/Fonts/malgun.ttf'
    wordcloud = WordCloud(font_path='static/AppleGothic.ttf',
                          relative_scaling=0.2,
                          background_color='white',
                          ).generate_from_frequencies(dict(data))

    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(img, format='png')
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()
