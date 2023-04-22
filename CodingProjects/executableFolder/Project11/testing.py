import math as m
import graphicsPlus as gr
from matrix import *
from hitbox import *

hitTrack = hitList()
enemyTrack = enemyLister()
spriteTrack = spriteLister()
targetTrack = targetLister()
hitDict = hitDic()
initInfo = (hitTrack,enemyTrack,spriteTrack,targetTrack,hitDict)
player = hitboxDefined((0,0),20,30,hitTrack,enemyTrack,spriteTrack,targetTrack,hitDict,"player",True)
activeBox = activeDamage(player,hitTrack)
enemyTrack.newType("Slime",5,20)

a = hitboxDefined((100,100),10,50,*initInfo,"Joe",False,"Slime")
b = hitboxDefined((-100,-100),50,10,*initInfo,"Moe",False,"Slime")
c = hitboxDefined((100,0),50,50,*initInfo,"Doe",False,"Slime")

activeBox.update()



a.move(30,30)
b.move(-30,-30)
c.move(-90,0)
player.move(10,0)



sdfgr = (player.collision(c))

asefdknjb = (activeBox.batchCheck())

c.deactivate()

activeBox.update()

dsfg = player.collision(c)

print(activeBox.batchCheck())