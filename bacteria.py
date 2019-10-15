import random
import math


class Bacteria(object):

    def __init__(self, MaxVel, Metabolism, SenseRange, MaxForce, PoisonAvoidence, PoisonInfluence, maxpose):


        self.VelXY  = [0, 0]
        self.AcelXY = [0, 0]
        self.Pose = [random.uniform(0, maxpose), random.uniform(0,maxpose)]
        self.lastpoison = []
        self.Targets = []
        self.TargetsIdx = []

        #bacs characteristics
        self.MaxVel = (0.8 * MaxVel + 0.2)
        self.Metabolism = (0.7 * Metabolism + 0.2)
        self.Force = (0.7 * MaxForce + 0.2)
        self.SenseRange = (0.4 * SenseRange + 0.2)
        self.PoisonAvoidence = PoisonAvoidence
        self.FoodEficiency = (self.Metabolism*0.55 + 0.4) # how much the bacteria utilize the food energy
        self.PoisonInfluence = (1.4*PoisonInfluence - 0.5)


        self.Color = [0, 255, 0]
        self.Desired = [0, 0]
        self.Steer = [0, 0]
        self.count  = 0
        self.Energy =1000
        self.Fit = 0

    def target(self, TargetPoseList):
        # a entrada será o vetor de posição da comida, e a saída deverá a força para redirecionar
        #self.count +=1

        if self.Energy > 0:
            self.Targets = []
            for i in range(len(TargetPoseList)):
                if TargetPoseList[i] not in self.lastpoison:
                    self.Targets.append(TargetPoseList[i])
            targets = []
            self.TargetsIdx = []
            for i in range(len(self.Targets)):
                d = math.sqrt((self.Pose[0] - self.Targets[i][0]) ** 2 + (self.Pose[1] - self.Targets[i][1]) ** 2)
                if d <= self.SenseRange:
                    targets.append([i, d])
            targets.sort(key=lambda x: x[1], reverse=False)

            for i in range(len(targets)):
                self.TargetsIdx.append(targets[i][0])

            if len(targets) == 0:
                self.seek([random.uniform(0, 1), random.uniform(0, 1)])
            else:
                if targets[0][1] > 0.005:
                    self.seek(self.Targets[targets[0][0]])
                    return None
                else:
                    return self.fit(self.Targets[targets[0][0]])

        else:
            self.Energy = 0
            return None


    def seek(self,targetData):
        self.Desired = [targetData[0]-self.Pose[0], targetData[1]-self.Pose[1]]

        mod = math.sqrt(self.Desired[0]**2+self.Desired[1]**2)

        desiredNor = [self.Desired[0]/mod, self.Desired[1]/mod]
        desiredNor = [desiredNor[0]*self.MaxVel, desiredNor[1]*self.MaxVel]

        self.Steer = [desiredNor[0]-self.VelXY[0], desiredNor[1]-self.VelXY[1]]
        force = math.sqrt(self.Steer[0]**2+self.Steer[1]**2)

        if force > self.Force:
            self.Steer[0] = self.Steer[0]*self.Force/force
            self.Steer[1] = self.Steer[1]*self.Force/force
        #print(self.Steer)
        self.update()


    def update(self):

        m =0.01

        self.AcelXY[0] = self.AcelXY[0] + self.Steer[0]
        self.AcelXY[1] = self.AcelXY[1] + self.Steer[1]

        self.VelXY[0] = self.VelXY[0]+0.01*self.AcelXY[0]
        self.VelXY[1] = self.VelXY[1]+0.01*self.AcelXY[1]

        vel = math.sqrt(self.VelXY[0]**2+self.VelXY[1]**2)

        if vel > self.MaxVel:

            self.VelXY[0] = self.VelXY[0]*self.MaxVelvel/vel
            self.VelXY[1] = self.VelXY[1]*self.MaxVelvel/vel

        #print(self.VelXY)

        self.Pose[0] = self.Pose[0] + 0.01*self.VelXY[0]
        self.Pose[1] = self.Pose[1] + 0.01*self.VelXY[1]

        #print(self.count)

        for i in range(len(self.Pose)):
            if self.Pose[i] > 1:
                self.Pose[i] = 1
            if self.Pose[i] < 0:
                self.Pose[i] = 0

        self.AcelXY = [0, 0]
        self.fit(0)


    def fit(self, data):
        self.Fit = self.Fit + 0.01

        if isinstance(data, list):
            if data[2] == 'F':
                self.Energy = self.Energy - 10 * math.sqrt(self.VelXY[0]**2+self.VelXY[1]**2) * self.Metabolism +\
                      100 * self.FoodEficiency
                self.updatecolor()
                return data
            else:
                if self.PoisonAvoidence > 0.5:
                    if data not in self.lastpoison:
                        self.lastpoison.append(data)
                        self.seek([random.uniform(0, 1), random.uniform(0, 1)])
                else:
                    self.Energy = self.Energy - 10 * math.sqrt(self.VelXY[0]**2+self.VelXY[1]**2) * self.Metabolism \
                                  - 300 * self.PoisonInfluence
                    return data


        else:
            self.Energy = self.Energy - 10 * math.sqrt(self.VelXY[0] ** 2 + self.VelXY[1] ** 2) * self.Metabolism
            self.updatecolor()
            return

    def updatecolor(self):
        r = 255 - self.Energy / 4
        g = self.Energy / 4

        if r > 255:
            r = 255
        if r < 0:
            r = 0

        if g > 255:
            g = 255
        if g < 0:
            g = 0
        self.Color = [r, g, 0]
        return()




#bac = bacteria(1, 1, 1)

