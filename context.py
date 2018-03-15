from nltk.tokenize import sent_tokenize
import re
from pprint import pprint

def main(text, keywords):
    sentences = sent_tokenize(text)
    #print(sentences)
    sentences = sentenceCleaning(sentences)
    n_sent = len(sentences)
    print("Searching for", keywords)
    occ = findOcc(sentences, keywords)
    freq = keywordFreq(text, keywords)

    #"""
    for k, value in occ.items():
            print("Found", len(value), "sentence occassions for keyword", k)
            if k != 'collocation':
                print("Found", len(freq[k]), "token occassions for keyword", k)
    print("\n")
    #pprint(occ['collocation'])
    #"""


    return occ, freq, n_sent

def findOcc(sentences, keywords):
    occ = dict()
    for keyword in keywords:
        occ[keyword] = []
    occ['collocation'] = []

    for sent in sentences:
        if all([re.search(r'\b'+keyword+r'[es]{0,2}\b', sent, re.IGNORECASE) for keyword in keywords]):
            occ['collocation'].append(sent)
        else:
            for keyword in keywords:
                if re.search(r'\b'+keyword+r'[es]{0,2}\b', sent, re.IGNORECASE):
                    occ[keyword].append(sent)
    print(occ)
    return occ

def keywordFreq(text, keywords):
    freq = dict()
    for keyword in keywords:
        freq[keyword] = re.findall(r'\b'+keyword+r'[es]{0,2}\b', text, re.IGNORECASE)
    return freq



def sentenceCleaning(sentences):
    for i in range(len(sentences)):
        sentences[i] = re.sub(r'(=){1,}\s.*\s(=){1,}', "", sentences[i])
    sentences = [sent.strip() for sent in sentences if len(sent) < 1000]
    sentences = [sent for sent in sentences if len(sent) > 1]
    sentences = [sent for sent in sentences if len(sent.split()) > 1]
    return sentences





if __name__ == '__main__':
    main()