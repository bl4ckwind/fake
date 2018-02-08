import wikipedia

def main():
    wikiSearch("Peregrin")


## Search wiki for n results. Query most likely
def wikiSearch(term):
    print("### WikiSearch ###")
    nikki_n = wikipedia.search(term, results=10)
    print(nikki_n)
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