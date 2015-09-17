#coding: utf-8
from scene import *

class MyScene ( Scene ):
def setup ( self):
self.x = self.size.w * 0.5
self.y = self.size.h * 0.5

def draw ( self ):
# 毎回、描画しないと通ったところに色が残ってしまう
background(0, 0, 0)
fill(1, 0, 0)
g = gravity ()
self.x += g.x * 100
self.y += g.y * 100
self.x = min ( self.size.w - 40, max( 0, self.x ))
self.y = min ( self.size.h - 40, max( 0, self.y ))
rect( self.x, self.y, 40, 40 )

fill(1, 1, 0)
w = 110
while(self.size.w > w):
h = 110
while(self.size.h > h ):
rect( w, h, 40, 40 )
h += 160
else:
w += 160

run( MyScene())
