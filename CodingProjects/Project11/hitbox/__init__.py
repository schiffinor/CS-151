'''

'''
import graphicsPlus as gr
import math as m
from shapely.geometry import Polygon
from matrix import *


def move(point,x,y):
    vector = matData(2,1,[[point[0]],[point[1]]])
    pointer = matData(2,1,[[x],[y]])
    movVec = vector+pointer
    movVec = (movVec.get(0,0),movVec.get(1,0))
    return movVec


def rotate(center,point,angle):
    center = matData([center[0]],[center[1]])
    vector = matData([point[0]],[point[1]])
    pointer = vector-center
    rotMat = matData(2,2,[[m.cos(angle),-m.sin(angle)],[m.sin(angle),m.cos(angle)]])
    rotPointer = rotMat*pointer
    rotVector = rotPointer+center
    rotVector = (rotVector.get(0,0),rotVector.get(1,0))
    return rotVector


class hitboxCalc:

    def __init__(self,center,input):
        file = gr.Image(gr.Point(0,0),input)
        colorMatrix = matData(file.getHeight(),file.getWidth())
        for i in range(file.getWidth()):
            for j in range(file.getHeight()):
                # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
                color = file.getPixel(i,j)
                # Add data to color matrix.
                if color ==[0,0,0]:
                    colorMatrix.set(j,i,0)
                else:
                    colorMatrix.set(j,i,1)
        self.mat = colorMatrix
    
    def __str__(self):
        return str(self.mat)


class hitboxDefined:

    def __init__(self,center,x,y,hitlist,enemyList,spriteList,targetList,hitDictionary,varName=None,player=False,enemyType=None,spriteType=None,boss=False,pWeapon=False,hitDeque=None):
        self.name = varName
        print(self.name)
        self.center = center
        self.bottomLeft = (center[0]-(.5)*x,center[1]-(.5)*y)
        self.bottomRight = (center[0]+(.5)*x,center[1]-(.5)*y)
        self.topLeft = (center[0]-(.5)*x,center[1]+(.5)*y)
        self.topRight = (center[0]+(.5)*x,center[1]+(.5)*y)
        self.boundingBox = Polygon([self.bottomLeft,self.bottomRight,self.topRight,self.topLeft])
        self.height = y
        self.width = x
        if self.name is not None:
            hitDictionary.newHit(self.name,self)
        else:
            hitDictionary.newHit("unnamedHitBox",self)
        self.state = True
        self.playerState = player
        self.enemyState = (False if enemyType == None else True)
        self.spriteState = (False if spriteType == None else True)
        self.bossState = boss
        self.weaponState = pWeapon
        if self.playerState == True and self.enemyState == False and self.spriteState == False and self.bossState == False and self.weaponState == False:
            pass
        elif self.playerState == False and self.enemyState == True and self.spriteState == False and self.bossState == False and self.weaponState == False:
            hitlist.add(self)
            if  (enemyType in enemyList.enemyDict.keys()) == True:
                enemyList.add([enemyList.enemyDict[enemyType],self])
            else:
                raise TypeError("You must first define the enemy type before appending hitboxes.")
        elif self.playerState == False and self.enemyState == False and self.spriteState == True and self.bossState == False and self.weaponState == False:
            hitlist.add(self)
            if  (spriteType in spriteList.enemyDict.keys()) == True:
                spriteList.add([spriteList.enemyDict[spriteType],self])
            else:
                raise TypeError("You must first define the sprite type before appending hitboxes.")
        elif self.playerState == False and self.enemyState == False and self.spriteState == False and self.bossState == True and self.weaponState == False:
            targetList.add(self)
        elif self.playerState == False and self.enemyState == False and self.spriteState == False and self.bossState == False and self.weaponState == True:
            pass
        elif sum[self.playerState,self.enemyState,self.spriteState,self.bossState,self.weaponState] != 1:
            raise ValueError("Hitbox can only be of one type.")
        else:
            raise ValueError("You're using this wrong!")

    def rotate(self,angle):
        self.bottomLeft = rotate(self.bottomLeft,self.center,angle)
        self.bottomRight = rotate(self.bottomRight,self.center,angle)
        self.topRight = rotate(self.topRight,self.center,angle)
        self.topLeft = rotate(self.topLeft,self.center,angle)
        self.boundingBox = Polygon([self.bottomLeft,self.bottomRight,self.topRight,self.topLeft])

    def move(self,x,y):
        self.center = tuple(map(lambda x,y: x+y,self.center,(x,y)))
        self.bottomLeft = move(self.bottomLeft,x,y)
        self.bottomRight = move(self.bottomRight,x,y)
        self.topLeft = move(self.topLeft,x,y)
        self.topRight = move(self.topRight,x,y)
        self.boundingBox = Polygon([self.bottomLeft,self.bottomRight,self.topRight,self.topLeft])

    def redefine(self,x,y):
        self.center = (x,y)
        self.bottomLeft = (self.center[0]-(.5)*self.width,self.center[1]-(.5)*self.height)
        self.bottomRight = (self.center[0]+(.5)*self.width,self.center[1]-(.5)*self.height)
        self.topLeft = (self.center[0]-(.5)*self.width,self.center[1]+(.5)*self.height)
        self.topRight = (self.center[0]+(.5)*self.width,self.center[1]+(.5)*self.height)
        self.boundingBox = Polygon([self.bottomLeft,self.bottomRight,self.topRight,self.topLeft])

    def activate(self):
        if self.state == True:
            raise ValueError("Already Enabled.")
        else:
            self.state = True
    
    def deactivate(self):
        if self.state == False:
            raise ValueError("Already Disabled.")
        else:
            self.state = False

    def collision(self,other):
        
        if self.boundingBox.intersects(other.boundingBox):
            collision = True
            collision = tuple([collision,other.name])
            return collision
        else:
            collision = False
            collision = tuple([collision])
            return collision

    def __str__(self):
        stringer = ("BL: "+str(self.bottomLeft)+"\n"+"BR: "+str(self.bottomRight)+"\n"+"TL: "+str(self.topLeft)+"\n"+"TR: "+str(self.topRight))
        return stringer


class hitList:

    def __init__(self):
        self.ref = []

    def add(self,other):
        self.ref.append(other)


class activeDamage:

    def __init__(self,player,damageList):
        self.master = damageList
        self.player = player
        self.active = []
        self.existing = damageList.ref
        self.inactive = []
    
    def update(self):
        self.existing = self.master.ref
        self.active = []
        self.inactive = []
        for fState in self.existing:
            if fState.state == True:
                self.active.append(fState)
            else:
                self.inactive.append(fState)
    
    def batchCheck(self):
        collisions = []
        for i in self.active:
            collisions.append(tuple(self.player.hitBox.collision(i)))
        return collisions


class activeTargets:

    def __init__(self,player,enemyList,targetList):
        self.player = player
        self.active = []
        self.existingEnemies = enemyList.ref
        self.existingTargets = targetList.ref
        self.inactive = []
    
    def update(self):
        self.active = []
        self.inactive = []
        for fState in self.existingEnemies:
            if fState[1].state == True:
                self.active.append(fState)
            else:
                self.inactive.append(fState)
        for fState in self.existingTargets:
            if fState[1].state == True:
                self.active.append(fState)
            else:
                self.inactive.append(fState)
    
    def batchCheck(self):
        collisions = []
        for i in self.active:
            collisions.append(self.player.collision(i))
        return collisions


class enemyLister:
    
    def __init__(self):
        self.ref = []
        self.enemyDict = {}

    def add(self,other):
        self.ref.append(other)

    def remove(self,entity):
        self.ref.remove(entity)

    def newType(self,name,damage,HP,frameList):
        stats = [name,damage,HP,frameList]
        self.enemyDict[name] = stats
    
    def __str__(self):
        return str(self.enemyDict)

    def damageCheck(self,attackBox):
        collisions = []
        for enemy in self.ref:
            if m.sqrt(((enemy.center[0]-attackBox.center[0])**2)+((enemy.center[1]-attackBox.center[1])**2)) <= (m.sqrt((attackBox.width**2)+(attackBox.height**2))/2):
                collisionState = attackBox.collision(enemy)
                if collisionState[0] == True:
                    collisions.append(enemy)
        for enemy in collisions:
            enemy.takeDamage(attackBox.damage)
        

        
class hitDic:

    def __init__(self):
        self.ref=[]
        self.hDic = {}

    def newHit(self,name,hitBox):
        self.hDic[name] = hitBox
        self.ref.append(name)
    
    def varRef(self,name):
        if name in self.hDic.keys() == True:
            return self.hDic[name]
        else:
            raise NameError("That name doesn't exist bro.\n Use '.newHit()'.")
    
    def __str__(self):
        return str(self.hDic)


class targetLister:

    def __init__(self):
        self.ref = []
        self.targetDict = {}

    def add(self,other):
        self.ref.append(other)

    def newType(self,name,HP):
        stats = [name,HP]
        self.targetDict[name] = stats
    
    def __str__(self):
        return str(self.targetDict)


class spriteLister:

    def __init__(self):
        self.ref = []
        self.spriteDict = {}

    def add(self,other):
        self.ref.append(other)

    def newType(self,name,damage):
        stats = [name,damage]
        self.spriteDict[name] = stats
    
    def __str__(self):
        return str(self.spriteDict)