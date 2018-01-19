import os
from pprint import pprint
import re
import json
import csv
import collections
import hashlib

def docReader(path_add):
    fn = os.path.join(os.path.dirname(__file__), path_add)
    return [fn + file for file in os.listdir(fn)]

def removeWithDate(processed_docs):
    keys = []
    for k, v in processed_docs.items():
        #print(processed_docs[k]['META']['DATE'])
        if int(processed_docs[k]['META']['DATE'].split(".")[2]) < 2010:
            keys.append(k)
        elif 'FULLTEXT' not in processed_docs[k].keys():
            keys.append(k)
    for key in keys:
        processed_docs.pop(key, None)
    return processed_docs

def IDMaker(data, printmedium):
    dic = dict()
    for k,v in data.items():
        date = data[k]['META']['DATE'].split(".")
        date = date[0] + date[1] + date[2][2:]
        ID = str(printmedium) + "_" + str(date) + "_1"
        i = 0
        sameday = [str(x) for x in range(100)]
        while ID in dic.keys():
            ID = re.sub(r'\d{1,3}$', sameday[i], ID)
            i += 1

        dic[ID] = data[k]
        if date == "160715":
            print(ID)

    return dic


def json_checksum(processed_docs):
    return hashlib.md5(json.dumps(processed_docs, sort_keys=True).encode('utf-8')).hexdigest()

def json_maker(processed_docs, filename):
    with open("JSON/" + filename, 'w', encoding="utf8") as f:
        json.dump(processed_docs, f)

def json_loader(filename):
    with open("JSON/" + filename + ".json", "r", encoding="utf8") as file:
        jsondump = json.load(file)
    with open("JSON/checksum_" + filename + ".txt", "r", encoding="utf8") as file:
        checksum = file.read().strip()
    if checksum == json_checksum(jsondump):
        print('Checksum:', checksum)
        return jsondump
    else:
        print("CHECKSUM ERROR")
        return 0

def json_search(jsondump, headline="", key="", value="", ID=""):
    print(key, value, ID)
    if ID:
        return jsondump[ID]
    else:
        for k,v in jsondump.items():
            if headline:
                if v['HEADLINE'].lower().strip() == headline.lower().strip():
                    return jsondump[k]
            if key:
                if v['META'][key] == value:
                    return jsondump[k]



def csv_reader(path, sep=","):
    dump = []
    with open(path, "r", encoding="utf8", newline="") as file:
        csvr = csv.reader(file, delimiter=sep)
        for row in csvr:
            if row:
                dump.append(row)
    return dump


def csv_maker(data, csvname, csvname_non):
    capt_aust = []
    capt_non_aust = []
    i=0 #regex matches
    wanted = ['DATE', 'SECTION', 'PAGE', 'BYLINE']
    for k,v in data.items():
        for c in data[k]['CAPTIONS']:
            match = re.search(r'[Aa]usterity', c)
            l = [data[k]['META'][w] for w in wanted]
            l.append(c)
            l.append(data[k]['HEADLINE'])
            if match:
                i +=1
                if l in [c[0:-2] for c in capt_aust]: #leave out DUPLICATE Columns to compare
                    l.append("DUPLICATE")
                else:
                    l.append("UNIQUE")
                if c in [c[-4] for c in capt_aust]:
                    l.append("CAPTIONDUPLICATE")
                else:
                    l.append("UNIQUE")
                capt_aust.append(l)
            else:
                if l in [c[0:-2] for c in capt_non_aust]:
                    l.append("DUPLICATE")
                else:
                    l.append("UNIQUE")
                capt_non_aust.append(l)
    #print(i)
    csvWriterExec(csvname, capt_aust, wanted)
    csvWriterExec(csvname_non, capt_non_aust, wanted)

def csv_maker2(data, csvname):
    entries = []
    wanted = ['DATE', 'PAGE', 'LENGTH']
    for k,v in data.items():
        l = [k]
        l += [data[k]['META'][w] for w in wanted]
        l.append(data[k]['HEADLINE'])
        if data[k]['CAPTIONS']:
            l.append(data[k]['CAPTIONS'])
        else:
            l.append('None')
        entries.append(l)
    header = ['ID']
    header += wanted
    header.append('HEADLINE')
    header.append('CAPTIONS')
    header.append('IMG')
    with open(os.path.dirname(__file__) + "\\CSV\\" + csvname, 'w', newline='\n') as file:
        writer = csv.writer(file, dialect='excel') 
        writer.writerow(header)
        for entry in entries:
            writer.writerow(entry)
        file.close()

def csvWriterExec(filename, captlist, wanted):
    header = wanted
    header.append('CAPTION')
    header.append('HEADLINE')
    header.append('DUPLICATE')
    header.append('CAPTIONDUPLICATE')
    with open(os.path.dirname(__file__) + "\\CSV\\" + filename, 'w') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(header)
        for entry in captlist:
            writer.writerow(entry)
        file.close()
    wanted = 0
    header = 0

def singleTextWriter(processed_docs, name):
    for k, v in processed_docs.items():
        with open(os.path.dirname(__file__) + '/corpus/' + name + '_singles/' + k + '.txt', 'w', encoding="utf8") as file:
        #with open(os.path.dirname(__file__) + '/corpus/cake/' + com + '/' + k + '.txt', 'w', encoding="utf8") as file:
                try:
                    processed_docs[k]['ARTICLE'] = re.sub(r'(Dokument\s\d{1,3}\svon\s\d{1,3})', '', processed_docs[k]['ARTICLE'])
                    file.write(processed_docs[k]['ARTICLE'])
                    file.close()

                except:
                    print("No article", k)
        file.close()


    

def dictSorter(dic):
    dic = collections.OrderedDict(sorted(dic.items()))
    for k, v in dic.items():
        dic[k] = collections.OrderedDict(sorted(dic[k].items()))
        dic[k]['META'] = collections.OrderedDict(sorted(dic[k]['META'].items()))
    return dic

def dateConverter(date):
    timestamp = None 
    timestamp = re.search(r'\d{1,2}:\d{1,2}\s(A|P)M', date)
    if timestamp:
        timestamp = timestamp.group()
    datedict = {"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10","November":"11" , "December":"12"}
    d = re.search(r'([A-Z][a-z]{1,})\s(\d{1,}),\s(\d{4})', date)
    day = d.group(2)
    if len(day) == 1:
        day = "0" + day

    date = day + "." + datedict[d.group(1)] + "." + d.group(3)

    return (date, timestamp)


def mainTextEditor(processed_docs):
    for k in processed_docs.keys():
        text = processed_docs[k]['FULLTEXT']
        text = re.sub(r'FULL TEXT', "", text)
        text = text.lstrip()
        text = re.sub(r'€', "EURO", text)
        text = re.sub(r'\(\s?EURO\s?\)', "EURO", text)
        text = re.sub(r'\[ ?EURO ?\]', "EURO", text)
        text = re.sub(r'£', "[POUND]", text)
        text = re.sub(r'\[ ?POUND ?\]', "POUND", text)
        text = re.sub(r'\(\s?POUND\s?\)', "POUND", text)
        processed_docs[k]['FULLTEXT'] = text
    return processed_docs

def sectionProblems(processed_docs, medium):
    """
    with open ("CSV/sections_problems.txt", "r") as file:
        csvr = csv.reader(file, delimiter="\t")
        for row in csvr:
            try:
                pprint(processed_docs[row[0]]["META"]["SECTION"])
            except:
                pass
    """
    print(len(processed_docs.keys()))
    with open('CSV/section.csv', 'r', encoding='utf8') as file:
        csvr = csv.reader(file, delimiter=';')
        csvr = list(csvr)
        for k, v in processed_docs.items():
            section = processed_docs[k]['META']['SECTION'].lower().replace(' ', '')
            #print(section)
            for row in csvr:
                if row[0] == medium:
                    if row[1] == section:
                        if row[-2] == '':
                            cat = 'online'
                        elif row[-2] == 'own':
                            cat = section
                        else:
                            cat = row[-2]
                        processed_docs[k]['META']['CATEGORY'] = cat
            if 'CATEGORY' not in processed_docs[k]['META'].keys():
                processed_docs[k]['META']['CATEGORY'] = 'online'
                        #print(processed_docs[k]['META']['CATEGORY'])
    return processed_docs


def progressBar(divisor, divident):
    progress = int(50*divident/divisor)
    print("[" + progress*"|" + (50-progress)*"." + "]")


if __name__ == "__main__":
    # execute only if run as a script
    main()
