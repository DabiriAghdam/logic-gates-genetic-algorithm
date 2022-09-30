#importing libraries
import pandas as pd
import random

#importing data
table = pd.read_csv("truth_table.csv")
gate_count = len(table.columns) - 2
goal = pow(2, gate_count + 1)
inputs = list()
for i in range(1, gate_count + 2):
    inputs.append(table["Input%d" % (i)])
result = table["Output"]

#utility funcs.
def output(gene,A,B):
    if (gene == "AND"):
        return A and B
    elif (gene == "NAND"):
        return not(A and B)
    elif (gene == "OR"):
        return A or B
    elif (gene == "NOR"):
        return not(A or B)
    elif (gene == "XOR"):
        return A ^ B
    elif (gene == "XNOR"):
        return not(A ^ B)

def printchromo(chromo):
    for k in range(0, len(chromo)):
        print(chromo[k],end=" ")
    print("\n")

def initialize(pop = 16):
    print("initial population - generation #0")
    init_pop = list()
    for _ in range(0, pop):
        gates = list()
        for _ in range(0, gate_count):
            gates.append(random.choice(["AND","NAND","OR","NOR","XOR","XNOR"]))
        init_pop.append(gates)
    return init_pop

def fitness(chromo):
    correct = 0
    for i in range(0, goal):
        out = output(chromo[0], inputs[0][i], inputs[1][i])
        for j in range(2, gate_count + 1):
            out = output(chromo[j - 1], out, inputs[j][i])
        if (out == result[i]): correct += 1 
    return correct

def crossover(mating_pool, pc = 0.75):
    new_pop = list()
    i = 0
    random.shuffle(mating_pool)
    l = len(mating_pool)
    while(i + 1 < l):
        if (random.random() <= pc):
            point = random.randint(0, gate_count + 1)
            genes1 = mating_pool[i]
            genes2 = mating_pool[i + 1]
            gates1 = list()
            gates1.extend(genes1[0:point])
            gates1.extend(genes2[point:])
            gates2 = list()
            gates2.extend(genes2[0:point])
            gates2.extend(genes1[point:])
            new_pop.append(gates1)
            new_pop.append(gates2)
        else:
            new_pop.append(mating_pool[i]) 
            new_pop.append(mating_pool[i + 1])
        i += 2
    if (l % 2 == 1): new_pop.append(mating_pool[l - 1])
    return new_pop

def mutate(chromo, pm = 0.06):
    new_genes = list()
    for gene in chromo:
        if (random.random() <= pm):
            new_gene = random.choice([item for item in ["AND", "NAND", "OR", "NOR", "XOR", "XNOR"] if item is not gene])
        else:
            new_gene = gene 
        new_genes.append(new_gene)
    return new_genes

def runme(pop = 16):
    init_pop = initialize(pop)
    init_pop_fitness = list()
    for i in range(0, len(init_pop)):
        fit = fitness(init_pop[i])
        init_pop_fitness.append(fit)
        if (fit == goal):
            print("***FOUND***")
            printchromo(init_pop[i])
            return
    print(max(init_pop_fitness))
    
    mutated_pop = init_pop 
    mutated_pop_fitness = init_pop_fitness
    count = 1
    while(True):
        print("generation #%d" %(count))
        count += 1
        sorted_pop = [x for _,x in sorted(zip(mutated_pop_fitness,mutated_pop))]
        mating_pool = random.choices(sorted_pop, weights=range(1,pop + 1), k = pop)
        
        new_pop = crossover(mating_pool)

        mutated_pop = list()
        for i in range(0, len(new_pop)):
            new_chromo = mutate(new_pop[i])
            mutated_pop.append(new_chromo)
        
        mutated_pop_fitness = list()
        for i in range(0, len(mutated_pop)):
            fit = fitness(mutated_pop[i])
            mutated_pop_fitness.append(fit)
            if (fit == goal):
                print("***FOUND***")
                printchromo(mutated_pop[i])
                return
        print(max(mutated_pop_fitness))

runme(pop = 16)
