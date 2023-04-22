'''
__init__.py
Roman Schiffino 151B Fall Semester
This is a module I wrote it basically defines a lot of super necessary classes such as my hitboxes, enemy trackers, and more. I think its pretty cool so check it out.
'''
import graphicsPlus as gr
import math as m
from shapely.geometry import Polygon
from matrix import *


def move(point,x,y):
    '''
    Defines move in the context of this module as a vector operation using my matrix module.
    '''
    vector = matData(2,1,[[point[0]],[point[1]]])
    pointer = matData(2,1,[[x],[y]])
    movVec = vector+pointer
    movVec = (movVec.get(0,0),movVec.get(1,0))
    return movVec


def rotate(center,point,angle):
    '''
    Defines rotate in the context of this module as a vector operation using my matrix module.
    This is for the hitboxes and would have been used for the boss moving hitboxes.
    '''
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
        '''
        Creates a very inefficient hitbox that perfectly matches the image. I scrapped this idea as I noticed it was way too inefficient and hard to work with.
        Ignore this.
        '''
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
        '''
        Crème de la crème, this is my hitbox class it is extremely useful and what this game mostly functions on.
        It registers the hitbox to different lists depending on the passed arguments. It is easily movable and easily allows for collision checking.
        It is fast and versatile and allows for efficient use in games. Wish I could've displayed its full potency by implementing the boss, but alas, time.
        '''
        self.name = varName
        # Originally for debugging, but thought, T'd leave it in so you could see how many enemies have been spawned.
        print(self.name)
        # Defines attributes of, and defines specific hitbox object. This is all the hitbox, but the bounding box xpecifically is what enabvles collsiion checking.
        self.center = center
        self.bottomLeft = (center[0]-(.5)*x,center[1]-(.5)*y)
        self.bottomRight = (center[0]+(.5)*x,center[1]-(.5)*y)
        self.topLeft = (center[0]-(.5)*x,center[1]+(.5)*y)
        self.topRight = (center[0]+(.5)*x,center[1]+(.5)*y)
        self.boundingBox = Polygon([self.bottomLeft,self.bottomRight,self.topRight,self.topLeft])
        self.height = y
        self.width = x
        # Registers everything to the dictionary of hitboxes.
        if self.name is not None:
            hitDictionary.newHit(self.name,self)
        else:
            hitDictionary.newHit("unnamedHitBox",self)
        # More parameters and attributes for the logic and to gain info on hitBox. I essentially wrote this syetem much in the way a module for distribution would be written,
        # ie to allow essentially anyone to use the system however they saw fit. This is partially because this is the first thing I wrote and I wasn't 100% on what I needed yet,
        # so I guess i over-engineered it.
        self.state = True
        self.playerState = player
        self.enemyState = (False if enemyType == None else True)
        self.spriteState = (False if spriteType == None else True)
        self.bossState = boss
        self.weaponState = pWeapon
        # Logic tree to register the hitbox to the right list and define properties correctly depending on the parameters passed.
        # This tree also makes sure that all pertinent information is passed and that enemy types exist before creating them.
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
        # These errors are again kind of to allow this to be used as a module by others, and I guess to remind myself of the usage of this module in case I mess up.
        elif sum[self.playerState,self.enemyState,self.spriteState,self.bossState,self.weaponState] != 1:
            raise ValueError("Hitbox can only be of one type.")
        else:
            raise ValueError("You're using this wrong!")

    def rotate(self,angle):
        '''
        Defines rotate for the hitbox using the rotate matrix function at the top.
        '''
        self.bottomLeft = rotate(self.bottomLeft,self.center,angle)
        self.bottomRight = rotate(self.bottomRight,self.center,angle)
        self.topRight = rotate(self.topRight,self.center,angle)
        self.topLeft = rotate(self.topLeft,self.center,angle)
        self.boundingBox = Polygon([self.bottomLeft,self.bottomRight,self.topRight,self.topLeft])

    def move(self,x,y):
        '''
        Defines move for the hitbox using the move matrix function at the top.
        '''
        self.center = tuple(map(lambda x,y: x+y,self.center,(x,y)))
        self.bottomLeft = move(self.bottomLeft,x,y)
        self.bottomRight = move(self.bottomRight,x,y)
        self.topLeft = move(self.topLeft,x,y)
        self.topRight = move(self.topRight,x,y)
        self.boundingBox = Polygon([self.bottomLeft,self.bottomRight,self.topRight,self.topLeft])

    def redefine(self,x,y):
        '''
        Redefines hitbox at a new center using the previously defined properties.
        '''
        self.center = (x,y)
        self.bottomLeft = (self.center[0]-(.5)*self.width,self.center[1]-(.5)*self.height)
        self.bottomRight = (self.center[0]+(.5)*self.width,self.center[1]-(.5)*self.height)
        self.topLeft = (self.center[0]-(.5)*self.width,self.center[1]+(.5)*self.height)
        self.topRight = (self.center[0]+(.5)*self.width,self.center[1]+(.5)*self.height)
        self.boundingBox = Polygon([self.bottomLeft,self.bottomRight,self.topRight,self.topLeft])

    def activate(self):
        '''
        Toggles hitBox activity on to be used with batch collision checkers.
        '''
        if self.state == True:
            raise ValueError("Already Enabled.")
        else:
            self.state = True
    
    def deactivate(self):
        '''
        Toggles hitBox activity off to be used with batch collision checkers.
        '''
        if self.state == False:
            raise ValueError("Already Disabled.")
        else:
            self.state = False

    def collision(self,other):
        '''
        Direct collision checker, ignores hitbox activity and directly checks if their is overlap between hitBoxes.
        '''
        # If statements are their to just format ouytput of this function.
        if self.boundingBox.intersects(other.boundingBox):
            collision = True
            collision = tuple([collision,other.name])
            return collision
        else:
            collision = False
            collision = tuple([collision])
            return collision

    def __str__(self):
        '''
        Defines how to output hitBox as string if told to print.
        '''
        stringer = ("BL: "+str(self.bottomLeft)+"\n"+"BR: "+str(self.bottomRight)+"\n"+"TL: "+str(self.topLeft)+"\n"+"TR: "+str(self.topRight))
        return stringer


class hitList:

    def __init__(self):
        '''
        Basic listing class to append all hitBoxes to.
        '''
        self.ref = []

    def add(self,other):
        '''
        Adds hitBox to list.
        '''
        self.ref.append(other)


class activeDamage:

    def __init__(self,player,damageList):
        '''
        Another list type class with a master. The master is a  list of all hitBoxes which can inflict damage on the player.
        This list grabs from the master list and when told to update will grab all active damage producing hitBoxes,
        check if they're active, if they are it'll add them to the active damage list.
        This enables batch checking damage for all active hitBoxes.
        '''
        self.master = damageList
        self.player = player
        self.active = []
        self.existing = damageList.ref
        self.inactive = []
    
    def update(self):
        '''
        Aforementioned update method.
        '''
        self.existing = self.master.ref
        self.active = []
        self.inactive = []
        for fState in self.existing:
            if fState.state == True:
                self.active.append(fState)
            else:
                self.inactive.append(fState)
    
    def batchCheck(self):
        '''
        Aforementioned batch checker.
        '''
        collisions = []
        for i in self.active:
            collisions.append(tuple(self.player.hitBox.collision(i)))
        return collisions


class activeTargets:

    def __init__(self,player,enemyList,targetList):
        '''
        Another list type class. Active targets are all hitBoxes which can be struck by the player.
        This is basically exactly the same as the active damage list but was deeemed unnecesary so its not updated and isn't really used. 
        As such I will not be commenting this any further.
        '''
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
        '''
        Yet another list type class. This class contains a dictionary of all enemy tpes with in it.
        Its use requires that before any enemy is added to the list its type be reistered first. 
        That is done with the newType method. This class is extyremely necessary as the enemies could not exist without it.
        '''
        self.ref = []
        self.enemyDict = {}

    def add(self,other):
        '''
        Adds enemy to list of all anemies.
        '''
        self.ref.append(other)

    def remove(self,entity):
        '''
        Removes enemy from list of all anemies.
        '''
        self.ref.remove(entity)

    def newType(self,name,damage,HP,frameList):
        '''
        Registers new type of enemy.
        '''
        stats = [name,damage,HP,frameList]
        self.enemyDict[name] = stats
    
    def __str__(self):
        '''
        String readout of enemyDictionary.
        '''
        return str(self.enemyDict)

    def damageCheck(self,attackBox):
        '''
        Essentially a damage check for all existing active enemies. Not really used as I felt memory and computation could be conserved by making fewer general batch checks.
        I make all these considerations for memory and computation saving because, I know this is a complex program, I also know that my PC is very much an outlier among home PCs.
        I have 128GB of very fast RAM, and 32 cores with 64 threads on a nearly server grade CPU with a top of the line GPU. I can only know how it runs on my PC and as such I hope runs ok for you.
        '''
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
        '''
        Yest another listing class, You only really need to initiate and pass this as all of its use is essentially internal.
        '''
        self.ref=[]
        self.hDic = {}

    def newHit(self,name,hitBox):
        '''
        Registers new hit to dictionary and reference list.
        '''
        self.hDic[name] = hitBox
        self.ref.append(name)
    
    def varRef(self,name):
        '''
        Checks if name passed is in the hit dictionary, if not raises error.
        '''
        if name in self.hDic.keys() == True:
            return self.hDic[name]
        else:
            raise NameError("That name doesn't exist bro.\n Use '.newHit()'.")
    
    def __str__(self):
        '''
        More string interpretation.
        '''
        return str(self.hDic)


class targetLister:

    def __init__(self):
        '''
        Ended up not being used except internally. I don;t believe this is used in the game code though, in any case this is for the boss,
        this is because in this case targets are defined as hitboxes taht can only recieve damage not deal it. I was going to define the boss
        as several hitboxes, some for striking and some for recieving damage, it would have been pretty cool.
        '''
        self.ref = []
        self.targetDict = {}

    def add(self,other):
        '''
        Same deal as before adding to reference list.
        '''
        self.ref.append(other)

    def newType(self,name,HP):
        '''
        Type registry.
        '''
        stats = [name,HP]
        self.targetDict[name] = stats
    
    def __str__(self):
        '''
        String interpretation.
        '''
        return str(self.targetDict)


class spriteLister:

    def __init__(self):
        '''
        Yet another list class. Sprites are the oposite definition of targets, in this case a sprite is a hitbox that can only deal damage not take it. 
        These were going to be boss arms, lasers, and energy balls. Same deal as all the other list classes. Except I really fleshed out the ones I used much more.
        For example, the enemy lister.
        '''
        self.ref = []
        self.spriteDict = {}

    def add(self,other):
        '''
        Add reference list.
        '''
        self.ref.append(other)

    def newType(self,name,damage):
        '''
        Type registry.
        '''
        stats = [name,damage]
        self.spriteDict[name] = stats
    
    def __str__(self):
        '''
        String interpretation.
        '''
        return str(self.spriteDict)