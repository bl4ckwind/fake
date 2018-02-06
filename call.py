import head
import tools

def main():
    train = []
    c = 0
    #truth = [1,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1]
    #"Frodo ", "Bilbo ", "Legolas ", "Gimli ", "Gandalf ", "Elrond ", "Aragorn ", "Boromir ", "Saruman "
    #"is a hobbit", "is an elf", "is a dwarf", "is a character", "is a maia"
    statements = [x + y for x in
                 ["Arwen "]
                    for y in 
                    ["is a hobbit", "is an elf", "is a dwarf", "is a character", "is a maia"]]
    print(len(truth), len(statements))
    
    for statement in statements:
        weights = head.main(statement)
        weights.insert(0, truth[c])
        train.append(weights)
        c+=1

    tools.csv_writer("test", train)



if __name__ == '__main__':
    main()