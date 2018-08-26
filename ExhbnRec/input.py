def art_input() :
    import pandas as pd

    western_data = pd.read_csv('static/western_preprocessed.csv')
    sample_data = western_data[['title', 'artist', 'image']].sample(25)

    return sample_data