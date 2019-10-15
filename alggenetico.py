import random

class Alggenetico(object):

    def __init__(self,MutRate):
        self.Resolution = 5
        self.MutRate = MutRate
        self.BacsSequenciadas = []
        self.Couples = []
        self.Parents = []
        self.Offspring = []
        self.NewGenCode = []


    def newoffspring(self, Parents):
        self.Parents = Parents
        SumEnergy = 0
        for i in range(len(self.Parents)):
            SumEnergy += Parents[i][0]

        for i in range(len(self.Parents)):
            self.Parents[i][0] = self.Parents[i][0]/SumEnergy
        self.genomaBin()
        return self.Offspring


    def genomaBin(self):
        for i in range(len(self.Parents)):
            bac = []
            bac.append(self.Parents[i][0])
            for j in range(1,7): # from 1 to the numer of characteristics minus 1
                #Genoma da caracteristca 1: velocidade range 0-1
                num = self.Parents[i][j]
                numb = int(num*31)
                gencod='{0:05b}'.format(numb)
                bac.append(gencod)
            self.BacsSequenciadas.append(bac)
        self.definecouple()

    def definecouple(self):

        self.Couples =[]

        for i in range(len(self.BacsSequenciadas)):
            Valor = random.uniform(0, 1)
            inflim = 0
            for j in range(len(self.BacsSequenciadas)):
                if inflim < Valor and Valor < (inflim+self.BacsSequenciadas[j][0]):
                    self.Couples.append(j)
                    break
                else:
                    inflim += self.BacsSequenciadas[j][0]

        for i in range(int(len(self.Couples)/2)):
            self.newgen(self.Couples[2*i], self.Couples[(2*i+1)])
        for i in range(len(self.NewGenCode)):
            self.Offspring.append(self.bintogen(self.NewGenCode[i]))
        #print(self.Offspring)

    def newgen(self, ParentA, ParentB):

        genParentA = self.BacsSequenciadas[ParentA][1]+self.BacsSequenciadas[ParentA][2]+\
                     self.BacsSequenciadas[ParentA][3]+self.BacsSequenciadas[ParentA][4]+\
                     self.BacsSequenciadas[ParentA][5]+self.BacsSequenciadas[ParentA][6]

        genParentB = self.BacsSequenciadas[ParentB][1] + self.BacsSequenciadas[ParentB][2] +\
                     self.BacsSequenciadas[ParentB][3] + self.BacsSequenciadas[ParentB][4]+\
                     self.BacsSequenciadas[ParentA][5] + self.BacsSequenciadas[ParentB][6]

        broken = random.randint(0,29)
        #broken = 5

        ProleA = genParentA[0:broken] + genParentB[broken:]
        ProleB = genParentB[0:broken] + genParentA[broken:]
        self.NewGenCode.append(self.mutation(ProleA))
        self.NewGenCode.append(self.mutation(ProleB))

    def mutation(self, prole):
        Mutation = random.uniform(0,1)
        if Mutation <= self.MutRate/100:
            cromtomut = random.randint(0,29)
            if prole[cromtomut] == '1':
                prole = prole[0:cromtomut]+"0"+prole[cromtomut+1:]
                return prole
            else:
                prole = prole[0:cromtomut] + "1" + prole[cromtomut+1:]
                return prole
        else:
            return prole

    def bintogen(self, prole):
        genbin = []
        for i in range(0,6):
            caracbin = prole[i*5:5*(i+1)]
            caracint = int(caracbin,2)/31
            genbin.append(caracint)
        return genbin






'''bacs = [[7, 1, 0.3, 0.4, 0.5, 0.3],
        [5, 1, 0.3, 0.4, 0.5, 0.3],
        [4, 1, 0.3, 0.4, 0.5, 0.3],
        [3, 1, 0.3, 0.4, 0.5, 0.3],
        [4, 1, 0.3, 0.4, 0.5, 0.3],
        [1, 1, 0.3, 0.4, 0.5, 0.3]]'''


#alg = Alggenetico(50)

#print(alg.newoffspring(bacs))



