import csv
from flask import Flask, render_template, flash, request


def simplify_text(text):
    for punctuation in ['.', ',', '!', '?', '"']:
        text = text.replace(punctuation, '')

    return text.lower()


def jaccard_similarity(text_a, text_b):
    word_set_a, word_set_b = [set(simplify_text(text).split())
                              for text in [text_a, text_b]]
    num_shared = len(word_set_a & word_set_b)
    num_total = len(word_set_a | word_set_b)
    return num_shared / num_total


def check_similarity(sample_1, sample_2, sample_3):
    content_list = [sample_1, sample_2, sample_3]
    similarity_list = []
    for text in range(len(content_list)):
        if text == 0:
            similarity = jaccard_similarity(content_list[0], content_list[1])
            similarity_list.append(similarity)
            similarity_text = jaccard_similarity(content_list[0], content_list[2])
            similarity_list.append(similarity_text)
        if text == 1:
            similarity_text = jaccard_similarity(content_list[1], content_list[2])
            similarity_list.append(similarity_text)
        
    with open('similarity matrix.csv', 'a') as input:
        writer = csv.writer(input)
        writer.writerow(similarity_list)

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def home():
    return render_template('textSimilarity.html')


@app.route("/similarity/", methods=["POST", "GET"])
def similarity():
    print(request.method)
    if request.method == 'POST':
        text_1 = request.form['content1']
        text_2 = request.form['content2']
        text_3 = request.form['content3']

        print(text_1, text_2)
        check_similarity(text_1, text_2, text_3)
        with open('similarity matrix.csv', 'r') as output:
            read = csv.reader(output)
            for row in read:
                one_comp = row[0]
                two_comp = row[1]
                three_comp = row[2]
                print(one_comp, two_comp, three_comp)
                break
    return render_template('result.html', First=one_comp, Second=two_comp, Third=three_comp)


if __name__ == "__main__":
    app.run()
