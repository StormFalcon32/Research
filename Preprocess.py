from nltk.corpus import stopwords
import re
import string
import csv
import pandas as pd
import gensim
import spacy


def clean(text):
    text = text.lower()
    # remove URLs
    text = re.sub(
        r'([\d\w]+?:\/\/)?([\w\d\.\-]+)(\.\w+)(:\d{1,5})?(\/\S*)?', ' ', text)
    # remove non ascii characters
    text = remove_non_ascii(text)
    # remove leading and trailing whitespace and merge extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def remove_non_ascii(s): return ''.join(i for i in s if ord(i) < 128)


def to_words(sentences):
    # tokenize and remove punctuation
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(sentence, deacc=True))


def remove_stopwords(tokenized_sentences, stop_words):
    for sentence in tokenized_sentences:
        filtered = [w for w in sentence if not w in stop_words]
        yield(filtered)


def lemmatize(tokenized_sentences, nlp):
    for sentence in tokenized_sentences:
        doc = nlp(' '.join(sentence))
        lemmatized = [w.lemma_ for w in doc]
        yield(lemmatized)


def main():
    nlp = spacy.load('en', disable=['parser', 'ner'])
    stop_words = set(stopwords.words('english'))
    csvIn = pd.read_csv(r'D:\Python\FatAcceptance\NoDups.csv')
    df = csvIn.to_dict('index')
    new = []
    for i in range(0, len(df)):
        num_retweets = df[i]['retweets']
        for _ in range(0, int(num_retweets + 1)):
            new.append(clean(df[i]['text']))
    # tokenize, remove stopwords, and lemmatize
    data_words = list(to_words(new))
    data_words = list(remove_stopwords(data_words, stop_words))
    data_words = list(lemmatize(data_words, nlp))
    with open(r'D:\Python\FatAcceptance\Lemmatized.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data_words)


if __name__ == '__main__':
    main()
