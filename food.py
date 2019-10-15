import random

class Food(object):

    def __init__(self, Nfood, MaxRange):
        self.Nfood = Nfood
        self.MaxRange = MaxRange
        self.FoodPose = []
        self.FoodPoseList = []
        self.insert(Nfood)

    def insert(self, Ninsert):
        for i in range(Ninsert):
            x = random.uniform(0, self.MaxRange)
            y = random.uniform(0, self.MaxRange)
            type = random.uniform(0, 1)
            if type <= 0.6:  # creat a food
                self.FoodPose = [x, y, 'F']
            else:
                self.FoodPose = [x, y, 'P']
            self.FoodPoseList.append(self.FoodPose)

    def withdraw(self,RemoveFood):
        self.FoodPoseList.remove(RemoveFood)
        self.insert(1)

    def updatefood(self, Nfood):
        self.FoodPoseList = []
        self.insert(Nfood)



#food = Food(5,1)

#print(food.FoodPoseList)


