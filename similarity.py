import csv
from math import *
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
            # similarity_list.append('1')
            similarity = jaccard_similarity(content_list[0], content_list[1])
            # print(f"The Jaccard similarity between: ",text ," and", text+1,f" equals {similarity:.4f}." "\n")
            similarity_list.append(similarity)
            similarity_text = jaccard_similarity(content_list[0], content_list[2])
            # print(f"The Jaccard similarity between: ",text ," and", text+2,f" equals {similarity_text:.4f}." "\n")
            similarity_list.append(similarity_text)
        if text == 1:
            # similarity = jaccard_similarity(content_list[1], content_list[0])
            # # print(f"The Jaccard similarity between: ",text ," and", text+2,f" equals {similarity:.4f}." "\n")
            # similarity_list.append(similarity)
            # similarity_list.append('1')
            similarity_text = jaccard_similarity(content_list[1], content_list[2])
            # print(f"The Jaccard similarity between: ",text ," and", text-1,f" equals {similarity_text:.4f}." "\n")
            similarity_list.append(similarity_text)
        # if text == 2:
        #     similarity = jaccard_similarity(content_list[2], content_list[0])
        #     # print(f"The Jaccard similarity between: ",text ," and", text-2,f" equals {similarity:.4f}." "\n")
        #     similarity_list.append(similarity)
        #     similarity_text = jaccard_similarity(content_list[2], content_list[1])
        #     # print(f"The Jaccard similarity between: ",text ," and", text-1,f" equals {similarity_text:.4f}." "\n")
        #     similarity_list.append(similarity_text)
        #     similarity_list.append('1')
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


# @app.route('/result/', methods=["POST", "GET"])
# def result():
#     return render_template('textSimilarity.html')


if __name__ == "__main__":
    app.run()


#
#
# if __name__ == '__main__':
#     sample_1 = "The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'll get points based on the cost of the products. You don't need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'll find the savings for you."
#     sample_2 = "The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you."
#     sample_3 = "We are always looking for opportunities for you to earn more points, which is why we also give you a selection of Special Offers. These Special Offers are opportunities to earn bonus points on top of the regular points you earn every time you purchase a participating brand. No need to pre-select these offers, we'll give you the points whether or not you knew about the offer. We just think it is easier that way."
    # webcrwal(sample_1, sample_2, sample_3)


    # with open('similarity matrix.csv', 'r') as readfile:
    #     list = [line.split('') for line in readfile]
    #     # for i in range(len(list[0])):
        #     for j in range(len(list[0])):
        #         cosine(list[i], list[j])


    #
    # word_count = pd.read_csv("F:/count.csv")
    # words = word_count.drop(columns=['data','mining'])
    # print(words)
    # print(words.columns)
    #
    #
    # # Normalize the data attributes for the Iris dataset.
    # normalized_X = preprocessing.normalize(words)
    #
    # print(normalized_X)
    # print(normalized_X[1,:])
    #
    # for i in range(5):
    #     for j in range(5):
    #         num = normalized_X[i, :]
    #         den = normalized_X[j, :]
    #         cosine(num,den)
