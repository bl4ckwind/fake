import head
import tools
import re

def main():


    truth = [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,
            0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,
            0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,
            0,0,0,0,0,1,0,
            0,0,1,0,0,0,0,
            0,0,0,1,0,0,0,0,0,0,1,0,0,0]
    #X = ["Gollum", "Bilbo Baggins", "Samwise Gamgee", "Peregrin Took", "Arwen", "Legolas", "Elrond", "Aragorn", "Denethor", "Boromir", "Faramir", "Treebeard", "Gimli", "Gandalf", "Saruman"]
    X = ["Donald Trump"]
    #Y = [" is a hobbit", " is an elf", " is a dwarf", " is a maia", " is an orc", " is an ent", " is a human"]
    Y = [" is a hobbit", " is an elf", " is a human", " is the president", " is an orange"]
    statements = [x + y for x in
                 X
                    for y in 
                    Y]
    print(len(truth), len(statements))

    # Load cached filenames
    cache = [re.search(r'wiki_(.*)\.txt', x).group(1) for x in tools.docReader("cache/")]

    result = execute(statements, cache, truth, False)

    tools.csv_writer("test_Donald", result)

def execute(statements, cache, truth, annotiert=False):
    result = []
    c = 0
    # Feature for each statment + manual annotation + caching
    for statement in statements:
        weights, subj = head.main(statement, cache)
        cache.append(subj)
        if annotiert:
            weights.insert(0, truth[c])
        result.append(weights)
        c+=1
    return result



if __name__ == '__main__':
    main()