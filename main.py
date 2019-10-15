from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from math import sin, cos, pi
import simpy.rt

import maingui
import pyqtgraph
from threading import Thread, Lock


import bacteria
import food
import alggenetico
import random

class ExampleApp(QtWidgets.QMainWindow, maingui.Ui_MainWindow):
    ola = QtCore.pyqtSignal()
    ola1 = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        pyqtgraph.setConfigOption('antialias', True)
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)

        self.btnBegin.clicked.connect(self.begin)

        self.FinishFlag = False
        self.btnFinish.clicked.connect(self.finish)
        self.btnFinish.setEnabled(False)

        self.TimeText.setEnabled(False)
        self.MaxFitText.setEnabled(False)
        self.GeneretionText.setEnabled(False)

        self.grPlot.plotItem.showGrid(True, True, 0.7)
        self.grPlot.plotItem.getViewBox().setMouseEnabled(False,False)
        self.grPlot.setYRange(0, 1)
        self.grPlot.setXRange(0, 1)

        self.Generations = 1

        self.MaxTime = 0

        self.bacs = []
        self.Time = 0
        self.Population = 0
        self.MaxFit = 0
        self.MutationRate = 0
        self.MaxEnergySum = 0

        #Sum of the gens

        self.MaxVelSum = 0
        self.MetabolismSum = 0
        self.ForceSum = 0
        self.SenseRangeSum = 0
        self.PoisonAvoidenceSum = 0
        self.PoisonInfluenceSum = 0

        #Avereage of the gens
        self.MaxVelSumAvg = []
        self.MetabolismSumAvg = []
        self.ForceSumAvg = []
        self.SenseRangeSumAvg = []
        self.PoisonAvoidenceAvg = []
        self.PoisonInfluenceAvg = []


        self.BestVel = []
        self.BestMetabolism = []
        self.BestSenseRange = []
        self.BestForce = []

        self.MaxEnergyMean = []
        self.MaxEnergy = []
        self.x = []

        self.ola.connect(self.draw)
        self.ola1.connect(self.UpdateInfos)

        self.mainMtx = Lock()
        self.mainTh = Thread(target=self.simTh)



    #def simulate(self):

    def finish(self):
        self.FinishFlag = True
        self.PopulationSpin.setEnabled(True)
        self.FoodSpin.setEnabled(True)
        self.TimeSpin.setEnabled(True)
        self.MutationRateSpin.setEnabled(True)
        self.btnBegin.setEnabled(True)
        self.TimeText.setEnabled(False)
        self.MaxFitText.setEnabled(False)
        self.GeneretionText.setEnabled(False)
        self.MutationRate = self.MutationRateSpin.value()

    def begin(self):
        self.Population = self.PopulationSpin.value()
        for i in range(self.Population):
            self.bacs.append(bacteria.Bacteria(random.uniform(0, 1),
                                               random.uniform(0, 1),
                                               random.uniform(0, 1),
                                               random.uniform(0, 1),
                                               random.uniform(0, 1),
                                               random.uniform(0, 1),
                                               1))
        self.food = food.Food(self.FoodSpin.value(), 1)
        self.MaxTime = self.TimeSpin.value()
        self.TimeText.setEnabled(True)
        self.MaxFitText.setEnabled(True)
        self.GeneretionText.setEnabled(True)
        self.btnFinish.setEnabled(True)
        self.PopulationSpin.setEnabled(False)
        self.FoodSpin.setEnabled(False)
        self.TimeSpin.setEnabled(False)
        self.MutationRateSpin.setEnabled(False)
        self.btnBegin.setEnabled(False)
        self.mainTh.start()
        self.alg = alggenetico.Alggenetico(self.MutationRate)

    def simTh(self):
        # simulation environment
        env = simpy.rt.RealtimeEnvironment(factor=1, strict=0)
        # simulation process definition
        proc = env.process(self.simulation(env))
        # simulation start
        env.run()

    def simulation(self, env):
        tm = 0
        while self.FinishFlag == False:
            if self.Time < self.MaxTime:
                self.mainMtx.acquire()

                for i in range(len(self.bacs)):
                    targetEated = (self.bacs[i].target(self.food.FoodPoseList))
                    if targetEated == None:
                         pass
                    else:
                        self.food.withdraw(targetEated)

                if tm > 0.1:
                    self.ola.emit()
                    tm = 0

                tm = tm + 0.01
                self.Time = self.Time + 0.01


                yield env.timeout(0.01)
                self.mainMtx.release()
            else:
                self.food.updatefood(self.FoodSpin.value())
                self.NewBacs()


    def NewBacs(self):
        #self.mainMtx.acquire()

        self.x.append(self.Generations)
        self.Generations = self.Generations + 1

        Parents = []

        #Energy = []
        for i in range(self.Population):
            Parents.append([self.bacs[i].Energy + self.bacs[i].Fit,
                            (self.bacs[i].MaxVel - 0.2)/0.8,
                            (self.bacs[i].Metabolism-0.2)/0.7,
                            (self.bacs[i].Force-0.2)/0.7,
                            (self.bacs[i].SenseRange-0.2)/0.4,
                            self.bacs[i].PoisonAvoidence,
                           (self.bacs[i].PoisonInfluence+0.5)/1.4])

        Parents.sort(key=lambda x: x[0], reverse=True)

        self.MaxEnergy.append(Parents[0][0])
        self.MaxEnergySum = self.MaxEnergySum + Parents[0][0]
        self.MaxEnergyMean.append(self.MaxEnergySum/(self.Generations-1))

        self.MaxVelSum = self.MaxVelSum + (Parents[0][1]*0.8+0.2)
        self.MaxVelSumAvg.append(self.MaxVelSum/(self.Generations-1))

        self.MetabolismSum = self.MetabolismSum + (Parents[0][2] * 0.7 + 0.2)
        self.MetabolismSumAvg.append(self.MetabolismSum / (self.Generations - 1))

        self.ForceSum = self.ForceSum + (Parents[0][3] * 0.7 + 0.2)
        self.ForceSumAvg.append(self.ForceSum/ (self.Generations - 1))

        self.SenseRangeSum = self.SenseRangeSum + (Parents[0][4] * 0.4 + 0.2)
        self.SenseRangeSumAvg.append(self.SenseRangeSum/ (self.Generations - 1))

        self.PoisonAvoidenceSum = self.PoisonAvoidenceSum + (Parents[0][5] * 0.8 + 0.2)
        self.PoisonAvoidenceAvg.append(self.PoisonAvoidenceSum / (self.Generations - 1))

        self.PoisonInfluenceSum = self.PoisonInfluenceSum + (Parents[0][6] * 1.4 - 0.5)
        self.PoisonInfluenceAvg.append(self.PoisonInfluenceSum/ (self.Generations - 1))

        self.BestVel.append(Parents[0][1])
        self.BestMetabolism.append(Parents[0][2])
        self.BestSenseRange.append(Parents[0][3])
        self.BestForce.append(Parents[0][4])
        print((Parents[0][1]*0.8+0.2), (Parents[0][2] * 0.7 + 0.2), (Parents[0][3] * 0.7 + 0.2),
              (Parents[0][4] * 0.4 + 0.2), (Parents[0][5] * 0.8 + 0.2), (Parents[0][6] * 1.4 - 0.5))
        self.MaxFit = round(max(self.MaxEnergy), 2)

        self.ola1.emit()
        self.bacs.clear()
        OffGen = self.alg.newoffspring(Parents)
        for i in range(self.Population):
            self.bacs.append(bacteria.Bacteria(OffGen[i][0],
                                               OffGen[i][1],
                                               OffGen[i][2],
                                               OffGen[i][3],
                                               OffGen[i][4],
                                               OffGen[i][5],
                                               1))

        self.Time = 0


    def UpdateInfos(self):

        self.GeneretionText.setPlainText(str(self.Generations))
        self.MaxFitText.setPlainText(str(self.MaxFit))

        self.grPlot.plotItem.plot(clear=True)
        self.grPlot_2.plotItem.showGrid(True, True, 0.7)
        self.grPlot_2.plotItem.getViewBox().setMouseEnabled(False,False)
        self.grPlot_2.setYRange(0, self.MaxFit+100)
        self.grPlot_2.setXRange(0, len(self.x))
        self.grPlot_2.plotItem.plot(self.x, self.MaxEnergy, pen=pyqtgraph.mkPen('b', width=1))
        self.grPlot_2.plotItem.plot(self.x, self.MaxEnergyMean, pen=pyqtgraph.mkPen('r', width=1))

        self.grPlot_3.plotItem.plot(self.x, self.MaxVelSumAvg, pen=pyqtgraph.mkPen('r', width=1))
        self.grPlot_3.plotItem.plot(self.x, self.MetabolismSumAvg, pen=pyqtgraph.mkPen('b', width=1))
        self.grPlot_3.plotItem.plot(self.x, self.ForceSumAvg, pen=pyqtgraph.mkPen('g', width=1))
        self.grPlot_3.plotItem.plot(self.x, self.SenseRangeSumAvg, pen=pyqtgraph.mkPen('k', width=1))
        self.grPlot_3.plotItem.plot(self.x, self.PoisonAvoidenceAvg, pen=pyqtgraph.mkPen('c', width=1))
        self.grPlot_3.plotItem.plot(self.x, self.PoisonInfluenceAvg, pen=pyqtgraph.mkPen('m', width=1))





    def draw(self):
        self.TimeText.setPlainText(str(round(self.Time, 3)))

        self.grPlot.plotItem.plot(clear=True)
        for i in range(len(self.food.FoodPoseList)):
            if self.food.FoodPoseList[i][2] == 'F':
                self.grPlot.plotItem.plot([self.food.FoodPoseList[i][0]], [self.food.FoodPoseList[i][1]], pen=None,
                                          symbolBrush = (0,0,255), symbol ='s')
            else:
                self.grPlot.plotItem.plot([self.food.FoodPoseList[i][0]], [self.food.FoodPoseList[i][1]], pen=None,
                                          symbolBrush=(255, 0, 0), symbol='s')

        #print(self.bac1.Pos)
        for i in range(len(self.bacs)):
            self.grPlot.plotItem.plot([self.bacs[i].Pose[0]], [self.bacs[i].Pose[1]], pen=None,
                                       symbolBrush = (self.bacs[i].Color[0], self.bacs[i].Color[1], self.bacs[i].Color[2]), symbol='o')

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")