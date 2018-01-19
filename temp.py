import tools
from nltk.tokenize import sent_tokenize
import re
from pycorenlp import StanfordCoreNLP
from pprint import pprint
#import wolframalpha.wap as wap

"""
Column 1: the ID of the statement ([ID].json).
Column 2: the label.
Column 3: the statement.
Column 4: the subject(s).
Column 5: the speaker.
Column 6: the speaker's job title.
Column 7: the state info.
Column 8: the party affiliation.
Column 9-13: the total credit history count, including the current statement.
9: barely true counts.
10: false counts.
11: half true counts.
12: mostly true counts.
13: pants on fire counts.
Column 14: the context (venue / location of the speech or statement).
"""

def main():
    nlp = StanfordCoreNLP('http://localhost:9000')
    data = tools.csv_reader("dataset/train.tsv", sep="\t")


    for row in data[0:25]:
        statement = row[2]
        sentences = sent_tokenize(statement)
        for sent in sentences:
            if re.search(r'\sis\s', sent):
                out = nlpRequest(nlp, sent)
                pprint(out)
                tokens = out['sentences'][0]['tokens']
                for token in tokens:
                    if 'ner' in token.keys():
                        print(token['ner'])



def nlpRequest(nlp, text):
    text = (text)
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,pos,regexner, depparse', # tokenize,ssplit,pos,depparse,parse
        'outputFormat': 'json'
        })

    return output

if __name__ == '__main__':
    main()
