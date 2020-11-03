import numpy as np

class Genetic(object):

    def __init__(self, f, pop_size = 100, n_variables = 2):
        self.f = f
        self.minim = -100
        self.maxim = 100
        self.pop_size = pop_size
        self.n_variables = n_variables
        self.population = self.initializePopulation()
        self.evaluatePopulation()

    def initializePopulation(self):
        return [np.random.randint(self.minim, self.maxim, size=(self.n_variables)) 
                           for i in range(self.pop_size)]

    def evaluatePopulation(self):
        return [self.f(i[0], i[1]) for i in self.population]
        #return [(i[0]-4)**2 + i[1]**2 for i in self.population]

    def nextGen(self):
        results = self.evaluatePopulation()
        children = [self.population[np.argmin(results)]]

        while len(children) < self.pop_size:
            # Tournament selection
            randA, randB = np.random.randint(0, self.pop_size), \
                           np.random.randint(0, self.pop_size)
            if results[randA] < results[randB]: p1 = self.population[randA]
            else: p1 = self.population[randB]

            randA, randB = np.random.randint(0, self.pop_size), \
                           np.random.randint(0, self.pop_size)  
            if results[randA] < results[randB]: p2 = self.population[randA]
            else: p2 = self.population[randB]   

            signs = []
            for i in zip(p1, p2):
                if i[0] < 0 and i[1] < 0: signs.append(-1)
                elif i[0] >= 0 and i[1] >= 0: signs.append(1)
                else: signs.append(np.random.choice([-1,1]))

            # Convert values to binary
            p1 = [format(abs(i), '010b') for i in p1]
            p2 = [format(abs(i), '010b') for i in p2]

            # Recombination
            child = []
            for i, j in zip(p1, p2):
                for k, l in zip(i, j):
                    if k == l: child.append(k)
                    else: child.append(str(np.random.randint(min(k, l), 
                                                             max(k,l))))

            child = ''.join(child)
            g1 = child[0:len(child)//2] 
            g2 = child[len(child)//2:len(child)]
            children.append(np.asarray([signs[0]*int(g1, 2), 
                                        signs[1]*int(g2, 2)]))
        self.population = children

    def run(self):
        ix = 0
        while ix < 1000:
            ix += 1
            self.nextGen()
        return self.population[0]

f = lambda x, y: 100 * (y**2) + 0.01 * abs(x + 100)
gen = Genetic(f)
minim = gen.run()
print('Minimum found      X =', minim[0], ', Y =', minim[1])