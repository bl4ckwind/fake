import wikipedia

def main():
    pass


def wikiSearch(term):
    print("### WikiSearch ###")
    nikki = wikipedia.search(term)
    print("# Found", len(nikki), "search results for", term, "#\n# Most likely:", nikki[0], "#")
    nikki = wikipedia.page(nikki[0])

    return nikki.content


if __name__ == '__main__':
    main()