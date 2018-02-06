import tools
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from pycorenlp import StanfordCoreNLP
from pprint import pprint
import networkx as nx
import wiki
import context
import wolfram
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
nlp = StanfordCoreNLP('http://localhost:9000')

def main(statement):

    """
    data = tools.csv_reader("dataset/train.tsv", sep="\t")
    sent = RowToSentences(data[1])
    """
    ### Analyse dependencies and parse them to a graph
    dep = analyseDependencies(statement, nlp)
    print("Satzlänge:", len(dep))
    G = DependenciesToGraph(dep)
    ### Determine SUBJ and OBJ of a is-sentence
    keywords = determineSubjObj(G) #subj 0, obj 1

    ### Get Wiki content and do context analysis
    #"""
    wikiContent = wiki.wikiSearch(keywords[0])
    wiki_n_occsent, wiki_n_token, wiki_n_sent = context.main(wikiContent, keywords)
    #"""

    ### Get WA content and do context analysis
    #"""
    WA_rawtext, WA_data, WA_assumptions = wolfram.main(keywords[0])
    WA_n_occsent, WA_n_token, WA_n_sent = context.main(WA_rawtext, keywords)
    #"""


    ### Compare syntax of collocation-sentences and root sentence
    #"""
    wiki_equal = equalSyntaxSentences(wiki_n_occsent, G)
    print("Sentences containing syntactic pattern:", len(wiki_equal), "\n")
    #print(euqalSS)
    #"""

    weights = weighter(keywords, wikiContent, wiki_n_occsent, wiki_n_token, wiki_n_sent, wiki_equal, WA_rawtext, WA_data, WA_assumptions, WA_n_occsent, WA_n_token, WA_n_sent)


    return weights

def nlpRequest(nlp, text, annotators):
    text = (text)
    output = nlp.annotate(text, properties={
        'annotators': annotators, # tokenize,ssplit,pos,depparse,parse
        'outputFormat': 'json'
        })

    return output

def weighter(keywords, wikiContent, wiki_n_occsent, wiki_n_token, wiki_n_sent, wiki_equal, WA_rawtext, WA_data, WA_assumptions, WA_n_occsent, WA_n_token, WA_n_sent):
    subj = keywords[0]
    obj = keywords[1]

    wiki_n_alltoken = len(word_tokenize(wikiContent))
    WA_n_alltoken = len(word_tokenize(WA_rawtext))

    ## WIKI WEIGHTS

    #1 Anzahl der Sätze, die das Objekt enthalten / Anzahl aller Sätze
    w_1 = len(wiki_n_occsent[obj]) / wiki_n_sent
    #2 Anzahl der Sätze, die das Objekt enthalten / Anzahl der Sätze, die das Subjekt enthalten
    w_2 = len(wiki_n_occsent[obj]) / len(wiki_n_occsent[subj])
    if w_2 > 1.0:
        w_2 = 1.0
    #3 Anzahl der Sätze die SUBJ und OBJ enthalten / Anzahl aller Sätze
    w_3 = len(wiki_n_occsent['collocation']) / wiki_n_sent
    #4 Anzahl der Sätze mit Kollokation und gleichem synt. Muster wie Eingabe / Anzahl der Sätze mit Kollokation
    if wiki_n_occsent['collocation']:
        w_4 = len(wiki_equal) / len(wiki_n_occsent['collocation'])
    else:
        w_4 = 0.0

    ## WOLFRAM WEIGHTS

    #5 Frequenz der Objekttokens / Alle Tokkens
    w_5 = len(WA_n_token[obj]) / WA_n_alltoken
    #6 Anzahl der Sätze mit Kollokation / Alle Sätze
    w_6 = len(WA_n_occsent['collocation']) / WA_n_sent

    #7 Weight for persons & fictional characters
    categories = ['Person', 'person', 'FictionalCharacter', 'fictional character']
    if WA_assumptions[0] in categories:
        w_7 = 1 if re.search(obj, WA_data['Basic information'], re.IGNORECASE) else 0
    else:
        w_7 = 0



    weights = [w_1,w_2,w_3,w_4,w_5,w_6,w_7]
    #weights = [weight * 5 if weight * 5 < 1 else weight for weight in weights]
    #multiplier = [3, 5, 4, 10, 4, 8, 10]
    #weights_perc = [(weight) * (100/sum(multiplier)*mult) for weight, mult in zip(weights, multiplier)]
    summa = 0
    print("Features")
    for i in range(len(weights)):
        print(weights[i])
        #print(weights_perc[i])
        #print("------")
        summa += weights[i]
    #print(summa)

    return weights






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



def compareSyntax(G, s):
    d = analyseDependencies(s, nlp)
    G2 = DependenciesToGraph(d)
    graphs = (G, G2)
    deps = [[], []]
    for i in range(2):
        for edge in list(graphs[i].edges):
            func1 = graphs[i].nodes[edge[0]]['dep']
            func2 = graphs[i].nodes[edge[1]]['dep']
            dep = (func1, func2)
            deps[i].append(dep)

    #Returns if all syntcatic dependencies of G are in G2
    return all([True if x in deps[1] else False for x in deps[0]])
                    

def equalSyntaxSentences(occ, G):
    equal = []
    for sent in occ['collocation']:
        equalSyntax = compareSyntax(G, sent)
        if equalSyntax:
            equal.append(sent)

    return equal

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
    # "is a hobbit", "is an elf", "is a dwarf", "is a character"
    main("Frodo is a hobbit")
