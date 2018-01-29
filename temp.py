import tools
from nltk.tokenize import sent_tokenize
import re
from pycorenlp import StanfordCoreNLP
from pprint import pprint
import networkx as nx
import wiki
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


    sent = RowToSentences(data[1])
    dep = analyseDependencies("President Obama is a Muslim", nlp)
    print("Satzlänge:", len(dep))
    G = DependenciesToGraph(dep)
    regenten = determineSubjObj(G)

    print(wiki.wikiSearch(regenten[0]))

   



def nlpRequest(nlp, text, annotators):
    text = (text)
    output = nlp.annotate(text, properties={
        'annotators': annotators, # tokenize,ssplit,pos,depparse,parse
        'outputFormat': 'json'
        })

    return output


def RowToSentences(row):
    statement = row[2]
    sentences = sent_tokenize(statement)
    return sentences

def analyseDependencies(sentence, nlp):
    out = nlpRequest(nlp, sentence, 'depparse')
    dependencies = out['sentences'][0]['basicDependencies']
    return dependencies

def DependenciesToGraph(dependencies):
    G = nx.Graph()
    #pprint(dependencies)
    for token in dependencies:
        G.add_node(token['dependent'], gov=token['governor'], token=token['dependentGloss'], dep=token['dep'])
    for token in dependencies:
        if token['governor'] != 0:
            G.add_edge(token['dependent'], token['governor'])
    #pprint(G.nodes.data())
    #pprint(G.edges)
    return G
        

def determineSubjObj(G):
    comp_subj = ""
    comp_obj = ""
    # ROOT is OBJ and NSUBJ is SUBJ
    for node in list(G.nodes):
        node_data = G.nodes[node]
        if node_data['dep'] == 'ROOT':
            obj = node
        if node_data['dep'] == 'nsubj':
            subj = node
    # Add compounds and adjectives to SUBJ/OBJ
    for node in list(G.nodes):
        node_data = G.nodes[node]
        if node_data['dep'] == 'compound' or node_data['dep'] == 'amod':
            #print("Found compound")
            if (node, node_data['gov']) in list(G.edges):
                if node_data['gov'] == obj:
                    comp_obj += node_data['token'] + " "
                if node_data['gov'] == subj:
                    comp_subj += node_data['token'] + " "

    comp_subj += G.nodes[subj]['token']
    comp_obj += G.nodes[obj]['token']

    print(comp_subj, comp_obj)
    return (comp_subj, comp_obj)




                    



    

def trash():
    for row in data:
        statement = row[2]
        sentences = sent_tokenize(statement)
        for sent in sentences:
            if re.search(r'\sis\s', sent) and len(sent) < 25:
                out = nlpRequest(nlp, sent, 'depparse')
                pprint(out)
                tokens = out['sentences'][0]['tokens']
                for token in tokens:
                    if 'ner' in token.keys():
                        print(token['ner'])
                
if __name__ == '__main__':
    main()
