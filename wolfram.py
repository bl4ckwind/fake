# 8J4HUE-59EKKAET95
import re
import xml.etree.ElementTree as ET
import requests
from pprint import pprint

def main(term):
    print("### Wolfram query ###")
    #"""
    interm = term
    appid = "8J4HUE-59EKKAET95"
    page = requests.get('http://api.wolframalpha.com/v2/query?input='
            + interm
            + '&appid='
            + appid)
    #with open("query.xml", "w", encoding="utf8") as file:
    content = str(page.content)[2:-1]
    content = content.replace('\\n', '')
    #    file.write(content)
    #"""
    #tree = ET.parse("query.xml")
    #tree = ET.fromstring(content)
    #print(content)
    rawtext, data, assumptions = outputFormatting(content)
    if assumptions:
        print("# Found", len(assumptions), "search results for", term, "#\n# Most likely:", assumptions[0], "#")
    else:
        print("# Found unambigous result")
        assumptions = [re.search(r'\((.*)\)', data['Input interpretation']).group(1)]
        #print(data)
    #print(rawtext)
    #print(assumptions)
    return rawtext, data, assumptions


def outputFormatting(output):
    data = dict()
    assumptions = []
    rawtext = ""
    root = ET.fromstring(output)
    for pod in root:
        for subpod in pod:
            for tag in subpod:
                if subpod.tag == 'assumption' and tag.tag == 'value':
                    assumptions.append(tag.attrib['name'])
                if tag.tag == 'plaintext':
                    data[pod.attrib['title']] = tag.text
                    if tag.text:
                        rawtext += tag.text.replace('|', '.')
    #pprint(data)
    #pprint(assumptions)
    return rawtext, data, assumptions

if __name__ == '__main__':
    main("Frodo")