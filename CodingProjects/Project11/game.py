import graphicsPlus as gr
import os
import sys
import numpy as np
import math as m
import tkinter as tk
import inspect as ins
import statistics as s
import time as t
import random as r
import bisect as b
from matrix import *
from hitbox import *
from threading import Timer, Thread, Lock
import json as js
from queue import Queue
from collections import deque
import pyglet as p
import ctypes


ctypes.windll.shcore.SetProcessDpiAwareness(2)
tick = 1/60
enemyLimit = 5
existingEnemies = []
hitTrack = hitList()
enemyTrack = enemyLister()
spriteTrack = spriteLister()
targetTrack = targetLister()
hitDict = hitDic()
hitTrackDeque = deque([hitTrack])
eyeDict = {}
slimeDict = {}
eyePathLists = {}
lootList = [None,None,None,None,None,"Heart","Heart","Heart","Sword","Sword","Shield"]
initInfo = (hitTrack,enemyTrack,spriteTrack,targetTrack,hitDict)
p.font.add_file("Project11\Horsemen Typeface\OTF\Horsemen.otf")



class Image(gr.Image):
    
    def __init__(self, p, *pixmap):
        gr.Image.__init__(self, p, *pixmap)

    def moveTo(self,x,y):
        prevCenter = self.getAnchor()
        prevCenter = (int(prevCenter.getX()),int(prevCenter.getY()))
        self.center = (x,y)
        deltas = tuple(map(lambda x,y: int(y-x), prevCenter,self.center))
        self.move(*deltas)


class positionTracker:

    def __init__(self):
        self._observers = []

    def notify(self,side,amount,exclusionList = []):
        for trackedEntity in self._observers:
            if trackedEntity not in exclusionList:
                trackedEntity.update(side,amount)

    def registerTracker(self,observer):
        if observer not in self._observers:
            self._observers.append(observer)
        else:
            raise ValueError("Already in tracker list.")

    def deregisterTracker(self,observer):
        if observer in self._observers:
            self._observers.remove(observer)
        elif observer == "All":
            self._observers = []
        else:
            raise ValueError("Not in tracker list.")


class Updater(positionTracker):

    def __init__(self):
        positionTracker.__init__(self)
        self._x_Pos = 0
        self._invarPos = 0

    def x_pos(self):
        return(self._x_Pos)
    
    def x_pos(self,new_x):
        self._x_Pos = new_x
        if self._x_Pos>610:
            if self._invarPos>=9250:
                if bg in self._observers and playerActor in self._observers:
                    positionAdapter.deregisterTracker(bg)
                    positionAdapter.deregisterTracker(playerActor)
            else:
                self.notify("R",self._x_Pos-610)
        if self._x_Pos<-610:
            if self._invarPos<=-610:
                if bg in self._observers and playerActor in self._observers:
                    positionAdapter.deregisterTracker(bg)
                    positionAdapter.deregisterTracker(playerActor)
            else:
                self.notify("L",self._x_Pos+610)
        if self._x_Pos>-610 and self._x_Pos<610 and self._invarPos<=9250:
            if bg not in self._observers and playerActor not in self._observers:
                    positionAdapter.registerTracker(bg)
                    positionAdapter.registerTracker(playerActor)
            else:
                pass

    def invarPos(self):
        return(self._invarPos)

    def invarPos(self,new_x):
        self._prevInvarPos = self._invarPos
        self._invarPos = new_x
        if self._invarPos>=9600:
            screen.unbind_all("<d>")
            screen.unbind_all("<d>" "<space>")
        elif self._invarPos<=-960:
            screen.unbind_all("<a>")
            screen.unbind_all("<a>" "<space>")
        elif self._prevInvarPos>=9600 and self._invarPos<9600:
            screen.bind_all("<d>", moveRight)
            screen.bind_all("<d>" "<space>", jumpRight)
        elif self._prevInvarPos>=-960 and self._invarPos<-960:
            screen.bind_all("<a>", moveLeft)
            screen.bind_all("<a>" "<space>", jumpLeft)
        else:
            if (self._prevInvarPos>=-960 and self._invarPos>-960) or (self._prevInvarPos<=9600 and self._invarPos<9600):
                pass
            else:
                raise RuntimeError("I don't think this should be possible.")


class weaponTracker:

    def __init__(self):
        self._observers = []

    def notify(self,state,exclusionList = []):
        for trackedEntity in self._observers:
            if trackedEntity not in exclusionList:
                trackedEntity.update2(state)

    def registerTracker(self,observer):
        if observer not in self._observers:
            self._observers.append(observer)
        else:
            raise ValueError("Already in tracker list.")

    def deregisterTracker(self,observer):
        if observer in self._observers:
            self._observers.remove(observer)
        elif observer == "All":
            self._observers = []
        else:
            raise ValueError("Not in tracker list.")


class Updater2(weaponTracker):

    def __init__(self):
        weaponTracker.__init__(self)
        self._playerWeaponActive = False
        self.playerWeaponPrevState = False

    def pActive(self):
        return(self._playerWeaponActive)
    
    def pActive(self,state):
        self.playerWeaponPrevState = self._playerWeaponActive
        self._playerWeaponActive = state
        if self._playerWeaponActive != self.playerWeaponPrevState:
            self.notify(state)
        else:
            pass


positionAdapter = Updater()
weaponUpdater = Updater2()
totalShield = deque([0])


def lootDrop(center):
    drop = r.choice(lootList)
    if drop is None:
        pass
    elif drop == "Heart":
        droppedHeart = Image(gr.Point(*center),"Project11\sprites\spriteGifs\heart.gif")
        droppedHeart.draw(screen)
        undrawer = Timer(1,droppedHeart.undraw)
        undrawer.start()
        playerActor.hitPoints += 25
    elif drop == "Sword":
        droppedSword = Image(gr.Point(*center),"Project11\sprites\spriteGifs\sword.gif")
        droppedSword.draw(screen)
        undrawer = Timer(1,droppedSword.undraw)
        undrawer.start()
        playerActor.damageUp(1.15)
    elif drop == "Shield":
        droppedShield = Image(gr.Point(*center),"Project11\sprites\spriteGifs\shield.gif")
        droppedShield.draw(screen)
        t.sleep(.5)
        droppedShield.move(800-center[0]-20*totalShield[0],450-center[1])
        playerActor.shieldUp(.9)
        totalShield[0] += 1
    else:
        pass


def attack_1():
    t.sleep(2*tick)
    weaponUpdater.pActive(True)
    playerActor.attackBox.activate()
    playerActor.attackImg.draw(screen)
    playerActor.standImg.undraw()
    screen.update


def attack_2():
    t.sleep(30*tick)
    weaponUpdater.pActive(False)
    playerActor.attackBox.deactivate()
    playerActor.standImg.draw(screen)
    playerActor.attackImg.undraw()
    screen.update


class player:
    
    def __init__(self,center):
        center = (int(center[0]),int(center[1]))
        self.absCenter = center
        self.center = center
        self.hitPoints = 100
        self.shieldRate = 1
        self.standImg = Image(gr.Point(*center),"Project11\characterDesigns\charpix2\playerCharStand.gif")
        self.attackImg = Image(gr.Point(*center),"Project11\characterDesigns\charpix2\playerCharAttack.gif")
        self.height = self.standImg.getHeight()
        self.width = self.standImg.getWidth()
        self.hitBox = hitboxDefined(center,self.standImg.getWidth()-50,self.standImg.getHeight(),*initInfo,"playerHit",True,hitDeque=hitTrackDeque)
        self.attackBox = hitboxDefined(((center[0]+75),(center[1])),75,self.standImg.getHeight()+50,*initInfo,"attackHit",False,None,None,False,True,hitDeque=hitTrackDeque)
        setattr(self.attackBox,"baseDamage",25)
        setattr(self.attackBox,"damage",self.attackBox.baseDamage)
        self.attackBox.deactivate()

    def attack(self):
        attackInit = Thread(target=attack_1,daemon=True)
        attackDeInit = Thread(target=attack_2,daemon=True)
        execList = list(locals())
        execList.remove('self')
        for i in execList:
            locals()[i].start()   
        
    def move(self,x,y):
        prevCenter = self.standImg.getAnchor()
        prevCenter = (int(prevCenter.getX()),int(prevCenter.getY()))
        self.standImg.move(x,y)
        self.attackImg.move(x,y)
        center = self.standImg.getAnchor()
        self.center = (int(center.getX()),int(center.getY()))
        deltas = tuple(map(lambda x,y: int(y-x), prevCenter,self.center))
        self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
        positionAdapter.x_pos(self.center[0])
        positionAdapter.invarPos(self.absCenter[0])
        self.hitBox.redefine(*self.center)
        self.attackBox.redefine(*map(lambda x,y: int(y+x), self.center,(75,0)))

    def moveTo(self,x,y):
        prevCenter = self.standImg.getAnchor()
        prevCenter = (int(prevCenter.getX()),int(prevCenter.getY()))
        self.center = (x,y)
        deltas = tuple(map(lambda x,y: int(y-x), prevCenter,self.center))
        self.standImg.move(*deltas)
        self.attackImg.move(*deltas)
        self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
        positionAdapter.x_pos(self.center[0])
        positionAdapter.invarPos(self.absCenter[0])
        self.hitBox.redefine(*self.center)
        self.attackBox.redefine(*map(lambda x,y: y+x, self.center,(75,0)))

    def adjust(self,x,y):
        self.standImg.move(x,y)
        self.attackImg.move(x,y)
        center = self.standImg.getAnchor()
        self.center = (int(center.getX()),int(center.getY()))
        positionAdapter.x_pos(self.center[0])
        self.hitBox.redefine(*self.center)
        self.attackBox.redefine(*map(lambda x,y: y+x, self.center,(75,0)))

    def update(self,side,amount):
        if side == "R":
            self.adjust(-2*amount,0)
        elif side == "L":
            self.adjust(-2*amount,0)
        else:
            raise ValueError("Only L or R.")
        screen.update()

    def damageCheck(self):
        damageSources.update()
        damages = damageSources.batchCheck()
        for damage in damages:
            if damage[0] == True:
                if damage[1][0] == "e":
                    self.hitPoints = self.hitPoints-self.shieldRate*eyeDict[damage[1]].attackDmg
                elif damage[1][0] == "s":
                    self.hitPoints = self.hitPoints-self.shieldRate*slimeDict[damage[1]].attackDmg
                if self.hitPoints<=0:
                    self.hitPoints = 0
                    break
        hitPointReadout.setText("HP: "+str(int(self.hitPoints)))
        screen.update()

    def damageUp(self,damageMult):
        self.attackBox.damage = self.attackBox.baseDamage*damageMult

    def shieldUp(self,shieldMult):
        self.shieldRate = self.shieldRate*shieldMult

    def draw(self):
        self.standImg.draw(screen)


class background:

    def __init__(self,center = (2.25*1920,0)):
        self.absCenter = center
        self.center = center
        self.body = Image(gr.Point(*center),"Project11\Resources\Background\Background.gif")

    def draw(self):
        self.body.draw(screen)

    def adjust(self,x,y):
        self.center = (self.center[0]+x,self.center[1]+y)
        self.body.move(x,y)

    def update(self,side,amount):
        if side == "R":
            self.adjust(-2*amount,0)
        elif side == "L":
            self.adjust(-2*amount,0)
        else:
            raise ValueError("Only L or R.")
        screen.update()


class enemy:

    def __init__(self,center,nameRef,enemylist,enemyType,frames):
        center = (int(center[0]),int(center[1]))
        self.nameRef = nameRef
        self.center = center
        self.absCenter = tuple(map(lambda x,y: int(y+x),self.center,playerActor.center))
        self.stats = enemylist.enemyDict[enemyType]
        self.type = enemyType
        self.name = self.stats[0]
        self.attackDmg = enemylist.enemyDict[enemyType][1]
        self.HP = enemylist.enemyDict[enemyType][2]
        self.enemyFrames = {}
        self.playerState = False
        for frame in range(frames):
            frameName = "frame"+str(frame)
            self.enemyFrames[frameName] = Image(gr.Point(*center),enemylist.enemyDict[enemyType][3][frame])
        self.hitBox = hitboxDefined(center,self.enemyFrames["frame0"].getWidth(),self.enemyFrames["frame0"].getHeight(),*initInfo,self.nameRef,enemyType=enemyType,hitDeque=hitTrackDeque)
        self.height = self.enemyFrames["frame0"].getHeight()
        self.width = self.enemyFrames["frame0"].getWidth()
        weaponUpdater.registerTracker(self)
        positionAdapter.registerTracker(self)
        spawnTool.maximalActiveEnemyQueue.put(self)

    def update(self,side,amount):
        if side == "R":
            self.adjust(-2*amount,0)
        elif side == "L":
            self.adjust(-2*amount,0)
        else:
            raise ValueError("Only L or R.")
        screen.update()

    def update2(self,state):
        self.playerState = state

    def adjust(self,x,y):
        center = self.enemyFrames["frame0"].getAnchor()
        self.center = (int(center.getX()),int(center.getY()))
        self.enemyFrames["frame0"].move(x,y)
        self.hitBox.redefine(*self.center)

    def localDmgCheck(self,attackBox):
        collisions = None
        if m.sqrt(((self.center[0]-attackBox.center[0])**2)+((self.center[1]-attackBox.center[1])**2)) <= 200 and playerActor.attackBox.state == True:
                collisionState = attackBox.collision(self.hitBox)
                if collisionState[0] == True:
                    callout = gr.Text(gr.Point(*tuple(map(lambda x,y: x+y,self.center,(0,75)))),"HIT!")
                    callout2 = gr.Text(gr.Point(*tuple(map(lambda x,y: x+y,self.center,(0,75)))),"HIT!")
                    callout.setFace("helvetica")
                    callout2.setFace("helvetica")
                    callout.setSize(24)
                    callout2.setSize(25)
                    callout.setFill("red")
                    callout2.setFill("black")
                    callout2.draw(screen)
                    callout.draw(screen)
                    undraw = Timer(.5,callout.undraw)
                    undraw2 = Timer(.5,callout2.undraw)
                    undraw.start()
                    undraw2.start()
                    self.takeDamage(attackBox.damage)
                    self.playerState = False

    def takeDamage(self,damage):
        self.HP = self.HP-damage
        if self.HP <= 0:
            self.die()        

    def die(self):
        center = self.center
        spawnTool.maximalActiveEnemyQueue.get()
        weaponUpdater.deregisterTracker(self)
        positionAdapter.deregisterTracker(self)
        self.hitBox.deactivate()
        existingEnemies.remove(self)
        for frame in range(len(self.enemyFrames)):
            frameName = "frame"+str(frame)
            self.enemyFrames[frameName].undraw()
            del self.enemyFrames[frameName]
        loot = Thread(target=lootDrop,args=[center],daemon=True)
        loot.start()
    
    def dieNoDrop(self):
        center = self.center
        spawnTool.maximalActiveEnemyQueue.get()
        weaponUpdater.deregisterTracker(self)
        positionAdapter.deregisterTracker(self)
        self.hitBox.deactivate()
        existingEnemies.remove(self)
        for frame in range(len(self.enemyFrames)):
            frameName = "frame"+str(frame)
            self.enemyFrames[frameName].undraw()
            del self.enemyFrames[frameName]

class eyeEnemy(enemy):

    def __init__(self,center,ref):
        enemy.__init__(self,center,ref,enemyTrack,"eyeBall",1)
        self.enemyFrames["frame0"].draw(screen)
    
    def move(self,pathPoints):
        smoothPath = pathPoints
        for i in range(len(pathPoints)-1):
            inpointDisplace = list(map(lambda x,y: (y-x),pathPoints[i],pathPoints[i+1]))
            stepDisplace = list(map(lambda x: x/2,inpointDisplace))
            for j in range(1):
                stepPoint = list(map(lambda x,y: int(x+((1)*y)),pathPoints[i],stepDisplace))
                smoothPath.append(stepPoint)
        smoothPath.sort(key=lambda x: m.sqrt((x[0]-playerActor.center[0])**2+(x[1]-playerActor.center[1])**2))
        start = t.time()
        for k in range(len(smoothPath)-1):
            if self.HP<=0:
                return
            t.sleep(tick*.000001)
            if self.HP<=0:
                return
            (dx,dy) = tuple(map(lambda x,y: -(y-x),smoothPath[k],smoothPath[k+1]))
            self.center = (self.center[0]+dx,self.center[1]+dy)
            self.absCenter = (self.center[0]+dx,self.center[1]+dy)
            if self.HP<=0:
                return
            self.enemyFrames["frame0"].move(dx,dy)
            self.hitBox.redefine(*self.center)
            screen.update()
            end = t.time()
            if self.playerState == True:
                self.localDmgCheck(playerActor.attackBox)
            timeElapsed = end-start
            if timeElapsed>.1:
                break


def eyeCreator(name, eyePos):
    if spawnTool.activityState == False:
        return
    eyeDict[name] = eyeEnemy(eyePos,name)
    existingEnemies.append(eyeDict[name])
    while eyeDict[name].HP > 0:
        distance = m.sqrt(((eyeDict[name].center[0]-playerActor.center[0])**2)+((eyeDict[name].center[1]-playerActor.center[1])**2))
        if distance <= 5:
            if eyeDict[name].HP <= 0:
                break
            t.sleep(1)
        if distance>5:
            if eyeDict[name].HP <= 0:
                break
            pathPasser = Timer(.9,pathGenerator,[name,eyeDict[name].center,playerActor.center,7,5])
            pathPasser.start()
            path = pathGenerator(name,eyeDict[name].center,playerActor.center,7,5)
            if eyeDict[name].HP <= 0:
                break
            eyeDict[name].move(path)
            if eyeDict[name].HP <= 0:
                break
            path = eyePathLists[name][0]


def qCheck(actor):
    for i in range(8):
        if actor.playerState == True:
            actor.localDmgCheck(playerActor.attackBox)
        t.sleep(5*tick)


class slimeEnemy(enemy):

    def __init__(self,center,slimeType,ref):
        enemy.__init__(self,center,ref,enemyTrack,slimeType,1)
        self.enemyFrames["frame0"].draw(screen)
    
    def move(self):
        self.playerCenter = playerActor.center
        directionVar = self.center[0]-self.playerCenter[0]
        if directionVar<0:
            sideStep = 1
        elif directionVar>0:
            sideStep = -1
        elif directionVar==0:
            sideStep = 0
        else:
            raise ValueError("Oi' mate this shouldn't be possible.")
        if abs(directionVar)>=180:
            directionVar = 180
            for i in range(-90,91):
                if self.HP<=0:
                    return
                upstep = (-i)/30
                newFoot = int(self.center[1]-int(self.height/2)+upstep)
                tempFloor = (540-floorData[960+sideStep+int(self.absCenter[0])][1])
                if self.HP<=0:
                    return
                prevCenter = self.enemyFrames["frame0"].getAnchor()
                prevCenter = (prevCenter.getX(),prevCenter.getY())
                self.enemyFrames["frame0"].move(sideStep,upstep)
                screen.update()
                if self.HP<=0:
                    return
                if newFoot+25<tempFloor:
                    break
                center = self.enemyFrames["frame0"].getAnchor()
                self.center = (int(center.getX()),int(center.getY()))
                deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
                self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
                self.hitBox.redefine(*self.center)
                if self.playerState == True:
                    self.localDmgCheck(playerActor.attackBox)
            prevCenter = self.enemyFrames["frame0"].getAnchor()
            prevCenter = (prevCenter.getX(),prevCenter.getY())
            if self.HP<=0:
                return
            self.enemyFrames["frame0"].moveTo(self.center[0],(540-int(floorData[960+int(self.absCenter[0])][1]-int(self.height/2))))
            screen.update()
            if self.HP<=0:
                return
            center = self.enemyFrames["frame0"].getAnchor()
            self.center = (int(center.getX()),int(center.getY()))
            deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
            self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
            self.hitBox.redefine(*self.center)
            if self.playerState == True:
                self.localDmgCheck(playerActor.attackBox)
        elif abs(directionVar)<180 and abs(directionVar)!=0:
            rangeTuple = (-int(abs(directionVar)/2),int(abs(directionVar)/2)+1)
            for i in range(*rangeTuple):
                upstep = (-i)/(m.ceil((abs(directionVar)/4)))
                newFoot = int(self.center[1]-int(self.height/2)+upstep)
                tempFloor = (540-floorData[961+int(self.absCenter[0])][1])
                if self.HP<=0:
                    return
                prevCenter = self.enemyFrames["frame0"].getAnchor()
                prevCenter = (prevCenter.getX(),prevCenter.getY())
                self.enemyFrames["frame0"].move(sideStep,upstep)
                screen.update()
                if self.HP<=0:
                    return
                if newFoot+25<tempFloor:
                    break
                center = self.enemyFrames["frame0"].getAnchor()
                self.center = (int(center.getX()),int(center.getY()))
                deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
                self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
                self.hitBox.redefine(*self.center)
                if self.playerState == True:
                    self.localDmgCheck(playerActor.attackBox)
                if self.HP<=0:
                    return
            prevCenter = self.enemyFrames["frame0"].getAnchor()
            prevCenter = (prevCenter.getX(),prevCenter.getY())
            if self.HP<=0:
                return
            self.enemyFrames["frame0"].moveTo(self.center[0],(540-int(floorData[960+int(self.absCenter[0])][1]-self.height/2)))
            screen.update()
            if self.HP<=0:
                return
            center = self.enemyFrames["frame0"].getAnchor()
            self.center = (int(center.getX()),int(center.getY()))
            deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
            self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
            self.hitBox.redefine(*self.center)
            if self.playerState == True:
                self.localDmgCheck(playerActor.attackBox)
        elif abs(directionVar)==0:
            for i in range(-90,91):
                upstep = (-i)/30
                newFoot = int(self.center[1]-int(self.height/2)+upstep)
                tempFloor = (540-floorData[961+int(self.absCenter[0])][1])
                if self.HP<=0:
                    return
                prevCenter = self.enemyFrames["frame0"].getAnchor()
                prevCenter = (prevCenter.getX(),prevCenter.getY())
                self.enemyFrames["frame0"].move(sideStep,upstep)
                screen.update()
                if self.HP<=0:
                    return
                if newFoot+25<tempFloor:
                    break
                center = self.enemyFrames["frame0"].getAnchor()
                self.center = (int(center.getX()),int(center.getY()))
                deltas = tuple(map(lambda x,y: y-x, prevCenter,self.center))
                self.absCenter = tuple(map(lambda x,y: int(y+x), self.absCenter,deltas))
                self.hitBox.redefine(*self.center)
                if self.playerState == True:
                    self.localDmgCheck(playerActor.attackBox)
        else:
            raise ValueError("Again this should be impossible. FYI most of these error messages are for debugging to trace erroe causes.")
        if self.playerState == True:
            self.localDmgCheck(playerActor.attackBox)
        interimTimer = Timer(5*tick,qCheck,[self])
        interimTimer.start()
        t.sleep(10*tick)
        if self.HP<=0:
            return
        t.sleep(r.random()*2)


def slimeCreator(name, slimePos):
    slimeType = r.choice(["greenSlime","greenSlime","greenSlime","blueSlime","blueSlime","purpleSlime"])
    if spawnTool.activityState == False:
        return
    slimeDict[name] = slimeEnemy(slimePos,slimeType,name)
    existingEnemies.append(slimeDict[name])
    while slimeDict[name].HP > 0:
        slimeDict[name].move()


class enemySpawner:

    def __init__(self):
        self.maximalActiveEnemyQueue = Queue(enemyLimit)
        self.activityState = True

    def spawn(self):
        self.spawnChoice = ["slime","slime","eyeBall"]
        self.enemyTypeChoice = r.choice(self.spawnChoice)
        if self.maximalActiveEnemyQueue.full() is not True:
            if self.enemyTypeChoice == "slime":
                x = r.randint(1000,2000)
                y = 600-floorData[960+int(playerActor.absCenter[0])+x][1]
                self.creator = Thread(target=slimeCreator,args=["slime"+str(len(slimeDict)),(x,y)],daemon=True)
                self.creator.start()
            elif self.enemyTypeChoice == "eyeBall":
                x = r.randint(-1200,1800)
                y = 540
                self.creator = Thread(target=eyeCreator,args=["eyeBall"+str(len(eyeDict)),(x,y)],daemon=True)
                self.creator.start()
            else:
                raise RuntimeError("Not possible, yo!")


def enemySpawnerThreader():
    global spawnTool
    spawnTool = enemySpawner()
    while spawnTool.activityState == True:
        t.sleep(2)
        if spawnTool.activityState == False:
            break
        spawnTool.spawn()


def screensize():
    scrGrab = tk.Tk()
    width = scrGrab.winfo_screenwidth()
    height = scrGrab.winfo_screenheight()
    scrGrab.destroy()
    return (width,height)


fov = 360
shapeList = []
screenParam = screensize()
'''
width = screenParam[0]
height = screenParam[1]
'''
width =1920
height=1080
# Honestly this logo is barely viible but I made the effort so here it is.
logo = tk.PhotoImage(file="Project05\Daco_6135086.png")
# We disable autoflush to decrease inefficiency, to prevent foreground flashing, and because it is bad.
screen = gr.GraphWin("Yeah, We Doin' a Project.'", width=width, height=height, autoflush=False)
screen.setCoords(-width/2,-height/2,width/2,height/2)
with open("Project11\FloorData.txt") as floorFile:
    floorData = js.load(floorFile)
floorFile.close()
floorData.extend([[10560, 899], [10561, 899], [10562, 899], [10563, 899], [10564, 899]])
playerActor = player((0,int(540-floorData[int(width/2)][1])+76))
bg = background()
damageSources =  activeDamage(playerActor,hitTrackDeque[0])


def restartProgram():
    os.execv(sys.executable, [sys.executable,__file__] + sys.argv)


def quitProgram():
    screen.destroy()
    exit()


def constantDamageCheck():
    while playerActor.hitPoints>0:
        t.sleep(5*tick)
        playerActor.damageCheck()
    print("You DIED!")
    spawnTool.activityState = False
    for item in existingEnemies:
        item.takeDamage(item.HP)
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    screen.unbind_all("<Control-space>")
    screen.unbind_all("<a>" "<space>")
    screen.unbind_all("<d>" "<space>")
    screen.unbind_all("<1>")
    flash()
    deathSplash = Image(gr.Point(0,0),"Project11\Resources\FAIL\gitGud.gif")
    deathSplash.draw(screen)
    restartGame = tk.Button(screen.master,text="RESTART?",activeforeground="black",activebackground="white",bd=0,command=restartProgram,bg="black",fg="white",font=("horsemen",25))
    quitGame = tk.Button(screen.master,text="Quit?",activeforeground="black",activebackground="white",bd=0,command=quitProgram,bg="black",fg="white",font=("horsemen",25))
    restartGame.pack()
    quitGame.pack()
    restartGame.place(anchor=tk.NE, x=675, y=800)
    quitGame.place(anchor=tk.NW, x=1225, y=800)


def screenFull(self, event=''):
    '''
    Sooooooo long story short this function right here gave me a lot of grief. I had hoped to make it just toggleable with <F11>;
    however, unfortunately when I made the function change the togglestate it broke everything... So just use <F11> to fullscreen and <Escape> to exit fullscreen.
    '''
    screen.master.attributes("-fullscreen", True)


def screenEsc(self, event=''):
    '''
    Same Story as above this is the toggle off function.
    '''
    screen.master.attributes("-fullscreen", False)


def flash():
    '''
    This function creates a "flash of light" effect that rapidly grows from the center of the screen
    and then disapears.
    '''
    # Initiates output list.
    tempList = []
    # Parameters for initial circle.
    center = gr.Point(0,0)
    radius = 1
    # Draw initial circle.
    flash = gr.Circle(center,radius)
    flash.setFill("black")
    tempList.append(flash)
    tempList[0].draw(screen)
    screen.update()
    radius = 0
    # Animation Loop.
    for i in range(50):
        # Updates radius and creates circle.
        radius += 40
        flash = gr.Circle(center,radius)
        flash.setFill("black")
        tempList.append(flash)
    for i in range(50):
        # Draws circle.
        tempList[i+1].draw(screen)
        screen.update()
    for i in range(51):
        # Removes all circles.
        tempList[i].undraw()
    screen.update()


def compColor(hexColor):
    '''
    This gets the complement to the initial color. 
    It is effectively the oposite or negative color. 
    That is that 255,255,255 "white" is the inputted color plus the returned color.
    Oh also I modified the Graphics plus package, getFill() command to return hex instead of tuples.
    This is because I prefer hex.
    ''' 
    # This takes an inputted string and removes the #
    modif = hexColor.lstrip("#")
    # Turns hex code into tuples in 255 format.
    tupColor = (int(modif[0:2], 16), int(modif[2:4], 16), int(modif[0:2], 16))
    # Calculates the complement color.
    complementColor = tuple(int(255-tupColor[i]) for i in range(len(tupColor)))
    # reformats tuple as hex.
    hexFormat = '#{:02x}{:02x}{:02x}'.format(*complementColor)
    # Returns hex color.
    return hexFormat


def pathGenerator(identifier,p1,pN,noiseLength=50,terminatingLength=50):
    eyePathLists[identifier] = deque()
    point0 = p1
    pointN = pN
    pointsList = []
    Length1 = m.sqrt(sum(map(lambda x,y: (y-x)**2,point0,pointN)))
    if Length1 <= terminatingLength:
        pointsList.append(pointN)
        eyePathLists[identifier].append(pointsList)
        return pointsList
    endState = False
    while endState == False:
        lengthState = False
        while lengthState == False:
            newPoint = tuple(map(lambda x,y: x+y, point0, (r.randint(-noiseLength,noiseLength),r.randint(-noiseLength,noiseLength))))
            Length2 = m.sqrt(sum(map(lambda x,y: (y-x)**2,newPoint,pointN)))
            if Length2<Length1:
                pointsList.append(newPoint)
                lengthState = True
        Length1 = Length2
        point0 = newPoint
        if Length2<terminatingLength:
            endState = True
    pointsList.append(pointN)
    eyePathLists[identifier].append(pointsList)
    return pointsList
    

def mountainBackground(color=0,y=0,roughness=0,displacement=0,iterations=0,beginx=(-.5)*width,endx=(.5)*width,floor=-10,varName=None):
    '''
    Woohoo, this was actually pretty fun. Difficult, but fun. Honestly I had to read a blogpost to get the idea for this algorithm. However, the implementation is my own.
    However, I doubt the implementation is too different from others because its a pretty unique idea. Basically a midpoint bisection algorithm.

    Also FYI this is compound shape 2.
    '''
    # This determines the x coordinates of the bounds of the mountain ranges depending on visible x coordinates in this screenspace dependant on z coordinates.
    x1 = beginx
    x2 = endx
    # Initiates our terrain array.
    pointList = [[x1,y],[x2,y]]
    grPointList = []
    # Splits our line however many times specified in iterations.
    for i in range(iterations):
        # Turns list to tuple because tuple values are better for this math.
        workablePoints = tuple(pointList)
        for j in range(len(workablePoints)-1):
            # Calculates midpoint x coordinate.
            midx = (workablePoints[j][0]+workablePoints[j+1][0])/2
            # Calculates midpoint y coordinate.
            midy = (workablePoints[j][1]+workablePoints[j+1][1])/2
            # Bundles these two values into a list like all other points.
            midpoint = list((midx,midy))
            # Changes the y value of the list.
            midpoint[1] += r.randrange(-1,1)*displacement
            # Prevents negative values.
            if midpoint[1] < floor:
                midpoint[1] = floor-(midpoint[1]-floor)
            # Puts the list into the right place in the list of lists. (Sorts by x coordinate.)
            b.insort(pointList,midpoint)
        # Lowers displacement paramater each iteration.
        displacement *= 2**(roughness)
    # Dynamically names and converts points to gr.Points. Then adds to grPointList.
    for i in range(len(pointList)):
        points = "point" + str(i+1)
        globals()[points] = tuple(pointList[i])
        grPoints = "grPoint" + str(i+1)
        globals()[grPoints] = gr.Point(*globals()[points])
        grPointList.append(globals()[grPoints])
    # Creates our desired polygon.
    backShape = gr.Polygon(*tuple(grPointList),gr.Point(x2,floor),gr.Point(x1,floor))
    # Sets color.
    backShape.setFill(color)
    # Handles naming when requested.
    if varName is not None:
        globals()[varName] = backShape
        return globals()[varName]


def quit(self):
    screen.close()
    exit()


def attack(self):
    screen.unbind_all("<1>")
    playerActor.attack()
    bind = Timer(30*tick,screen.bind_all, ["<1>", attack])
    bind.start()


def moveLeft(self):
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    time1 = Timer(.5*tick,screen.bind_all,["<d>", moveRight])
    time1.start()
    if positionAdapter._invarPos>=-960:
        time2 = Timer(.5*tick,screen.bind_all,["<a>", moveLeft])
        time2.start()
    for i in range(5):
        if positionAdapter._invarPos<=-960:
            break
        center = playerActor.absCenter
        height = playerActor.height
        dx = -1
        dy = (540-floorData[int(center[0])+961][1])+height/2-center[1]
        playerActor.move(dx,dy)
        screen.update()
        

def moveRight(self):
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    time1 = Timer(.5*tick,screen.bind_all,["<a>", moveLeft])
    time1.start()
    if positionAdapter._invarPos<=9600:
        time2 = Timer(.5*tick,screen.bind_all,["<d>", moveRight])
        time2.start()
    for i in range(5):
        if positionAdapter._invarPos>=9600:
            break
        center = playerActor.absCenter
        height = playerActor.height
        dx = 1
        dy = (540-floorData[int(center[0])+961][1])+height/2-center[1]
        playerActor.move(dx,dy)
        screen.update()
        

def jumpUp(self):
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    screen.unbind_all("<Control-space>")
    screen.unbind_all("<a>" "<space>")
    screen.unbind_all("<d>" "<space>")
    for i in range(-90,91):
        upstep = (-i)/30
        playerActor.move(0,upstep)
        screen.update()
    screen.bind_all("<a>", moveLeft)
    screen.bind_all("<d>", moveRight)
    screen.bind_all("<a>" "<space>", jumpLeft)
    screen.bind_all("<Control-space>", jumpUp)
    screen.bind_all("<d>" "<space>", jumpRight)


def jumpLeft(self):
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    screen.unbind_all("<Control-space>")
    screen.unbind_all("<a>" "<space>")
    screen.unbind_all("<d>" "<space>")
    stepSet = None
    for i in range(-90,91):
        if positionAdapter._invarPos<=-960:
            stepSet = i
            break
        upstep = (-i)/30
        newFoot = playerActor.center[1]-playerActor.height/2+upstep
        tempFloor = (540-floorData[960+int(playerActor.absCenter[0])][1])
        playerActor.move(-1,upstep)
        screen.update()
        if newFoot+25<tempFloor:
            break
    if stepSet is not None:
        for j in range(stepSet+1,91):
            upstep = (-j)/30
            newFoot = playerActor.center[1]-playerActor.height/2+upstep
            tempFloor = (540-floorData[960+int(playerActor.absCenter[0])][1])
            playerActor.move(0,upstep)
            screen.update()
            if newFoot+25<tempFloor:
                break
    if newFoot>tempFloor:
        playerActor.move(0,tempFloor-newFoot)
    screen.update()
    screen.bind_all("<d>", moveRight)
    screen.bind_all("<d>" "<space>", jumpRight)
    screen.bind_all("<Control-space>", jumpUp)
    if positionAdapter._invarPos>=-960:
        screen.bind_all("<a>", moveLeft)
        screen.bind_all("<a>" "<space>", jumpLeft)


def jumpRight(self):
    screen.unbind_all("<a>")
    screen.unbind_all("<d>")
    screen.unbind_all("<Control-space>")
    screen.unbind_all("<a>" "<space>")
    screen.unbind_all("<d>" "<space>")
    stepSet = None
    for i in range(-90,91):
        if positionAdapter._invarPos>=9600:
            stepSet = i
            break
        upstep = (-i)/30
        newFoot = playerActor.center[1]-playerActor.height/2+upstep
        tempFloor = (540-floorData[960+int(playerActor.absCenter[0])][1])
        playerActor.move(1,upstep)
        screen.update()
        if newFoot+25<tempFloor:
            break
    if stepSet is not None:
        for j in range(stepSet+1,91):
            upstep = (-j)/30
            newFoot = playerActor.center[1]-playerActor.height/2+upstep
            tempFloor = (540-floorData[960+int(playerActor.absCenter[0])][1])
            playerActor.move(0,upstep)
            screen.update()
            if newFoot+25<tempFloor:
                break
    if newFoot>tempFloor:
        playerActor.move(0,tempFloor-newFoot)
    screen.update()
    screen.bind_all("<a>", moveLeft)
    screen.bind_all("<a>" "<space>", jumpLeft)
    screen.bind_all("<Control-space>", jumpUp)
    if positionAdapter._invarPos<=9600:
        screen.bind_all("<d>", moveRight)
        screen.bind_all("<d>" "<space>", jumpRight)


def main():
    # Unfortunately because of tkinters scaling, which I only found out about too late. I have to use not 1080p, and I got around that by creating a fullscreen function.
    #Regardless lead to not as clean an ouput as I had hoped.
    global hitPointReadout
    enemyTrack.newType("eyeBall",10,30,["Project11\characterDesigns\charGifs\eye.gif"])
    enemyTrack.newType("greenSlime",5,15,["Project11\characterDesigns\charGifs\greenSlimeF1.gif","Project11\characterDesigns\charGifs\greenSlimeF2.gif","Project11\characterDesigns\charGifs\greenSlimeF3.gif","Project11\characterDesigns\charGifs\greenSlimeF4.gif"])
    enemyTrack.newType("blueSlime",10,20,["Project11\characterDesigns\charGifs\BlueSlimeF1.gif","Project11\characterDesigns\charGifs\BlueSlimeF2.gif","Project11\characterDesigns\charGifs\BlueSlimeF3.gif","Project11\characterDesigns\charGifs\BlueSlimeF4.gif"])
    enemyTrack.newType("purpleSlime",15,35,["Project11\characterDesigns\charGifs\purpleSlimeF1.gif","Project11\characterDesigns\charGifs\purpleSlimeF2.gif","Project11\characterDesigns\charGifs\purpleSlimeF3.gif","Project11\characterDesigns\charGifs\purpleSlimeF4.gif"])
    spawnThread = Thread(target=enemySpawnerThreader,daemon=True)
    spawnThread.start()
    screen.bind_all("<F11>", screenFull)
    screen.bind_all("<Escape>", screenEsc)
    screen.bind_all("<Delete>", quit)
    screen.bind_all("<1>", attack)
    screen.bind_all("<a>", moveLeft)
    screen.bind_all("<d>", moveRight)
    screen.bind_all("<Control-space>", jumpUp)
    screen.bind_all("<a>" "<space>", jumpLeft)
    screen.bind_all("<d>" "<space>", jumpRight)
    # Sets Icon.
    screen.master.iconphoto(False, logo)
    # Sets inital screenstate as not fullscreen.
    screen.master.attributes("-fullscreen", False)
    bg.draw()
    playerActor.draw()
    hpBox = gr.Rectangle(gr.Point(-955,535),gr.Point(-750,490))
    hpBox.setFill("white")
    hitPointReadout = gr.Text(gr.Point(-850,513),("HP: "+str(int(playerActor.hitPoints))))
    hitPointReadout.setFace("helvetica")
    hitPointReadout.setSize(25)
    hpBox.draw(screen)
    hitPointReadout.draw(screen)
    hitTracker = Thread(target=constantDamageCheck,daemon=True)
    hitTracker.start()
    positionAdapter.registerTracker(bg)
    positionAdapter.registerTracker(playerActor)
    tk.mainloop()


main()