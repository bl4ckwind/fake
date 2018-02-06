import wikipedia

def main():
    wikiSearch("Peregrin")


def wikiSearch(term):
    print("### WikiSearch ###")
    nikki_n = wikipedia.search(term, results=10)
    try:
        best = nikki_n[0]
        nikki = wikipedia.page(best)
    except:
        best = nikki_n[1]
        nikki = wikipedia.page(best)
    print("# Found", len(nikki_n), "search results for", term, "#\n# Most likely:", best, "#")

    return nikki.content


if __name__ == '__main__':
    main()