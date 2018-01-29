from nltk.tokenize import sent_tokenize
import re

def main(text, keyword):
    sentences = sent_tokenize(text)
    occ = findOcc(sentences, keyword)

def findOcc(sentences, keyword):
    occ = []
    for sent in sentences:
        if re.search(keyword, sent, re.IGNORECASE):
            occ.append(sent)
    return occ



if __name__ == '__main__':
    main()