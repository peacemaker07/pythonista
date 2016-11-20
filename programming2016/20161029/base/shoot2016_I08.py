#coding: utf-8

from scene import *
import sound
import random
import time
from math import sin,cos,pi


A=Action


standing_texture=Texture('plf:AlienBeige_front')
walk_textures=[Texture('plf:AlienBeige_climb1'),
Texture('plf:AlienBeige_climb2')]

game_duration=60

class Meteor (SpriteNode):
	def __init__(self,**kwargs):
		img=random.choice(['plf:Tile_BrickBrown','plf:Tile_BrickGrey'])
		SpriteNode.__init__(self,img,**kwargs)
		self.destroyed=False
			
class GameScene(Scene):
	
	def setup(self):
		
		ground=Node(parent=self)
		
		self.player=SpriteNode(standing_texture)
		self.player.anchor_point=(0.5,0)
		self.add_child(self.player)
		
		score_front=('Futura',40)
		self.score_label=LabelNode('0',score_front,parent=self)
		self.score_label.position = (self.size.w/2, self.size.h - 70)
		self.score_label.z_position = 5
		
		time_font=('Futura',40)
		self.time_label=LabelNode('00:00',time_font,parent=self)
		self.time_label.position=(self.size.w/3,self.size.h-70)
		self.time_label.z_position=5
		
		self.items=[]
		
		self.lasers=[]
		
		self.new_game()
		
	def new_game(self):
		
		self.background_color='#004f82'
		
		self.items=[]
		self.lasers=[]
		
		self.score = 0
		self.score_label.text = '0'
		
		self.start_time=time.time()
		
		
		self.walk_step=-1
		
		self.player.position=(self.size.w/2,10)
		self.player.texture=standing_texture
		self.speed=1.0
		
		self.spawn_item()
		
	def update(self):
		
		self.update_player()
		
		self.check_laser_collisions()
		
		time_passed=time.time()-self.start_time
		t=max(0,int(game_duration-time_passed))
		self.time_label.text='{0}:{1:0>2}'.format(t/60,t%60)
		
	def touch_began(self,touch):
		
		self.shoot_laser()
	

												
																																								

	def update_player(self):
		# iPadの傾きを取得
		g = gravity()
		if abs(g.x) > 0.05:
			self.player.x_scale = cmp(g.x, 0)
			x = self.player.position.x
			max_speed = 40
			x = max(0, min(self.size.w, x + g.x * max_speed))
			self.player.position = (x, 10)

			step = int(self.player.position.x / 40) % 2
			
			if step != self.walk_step:
				# プレイヤーを歩いている状態にする
				self.player.texture = walk_textures[step]
				
				sound.play_effect('rpg:Footstep00', 0.05, 1.0 + 0.5 * step)
				self.walk_step = step
		else:
			# プレイヤーを立っている状態にする
			self.player.texture = standing_texture
			self.walk_step = -1
			
	def check_laser_collisions(self):
		for laser in list(self.lasers):
			
			if not laser.parent:
				self.lasers.remove(laser)
				continue
				
			for item in self.items:
				
				if laser.position in item.frame:
					self.lasers.remove(laser)
					laser.remove_from_parent()
					self.destroy_meteor(item)
					break
					
	def destroy_meteor(self,meteor):
		sound.play_effect('arcade:Explosion_2,0.2')
		
		meteor.remove_from_parent()
		self.items.remove(meteor)
		
		self.score += 10 
		self.score_label.text=str(self.score)
		
		
		
		for i in xrange(5):
			m=SpriteNode('spc:MeteorBrownMed1',parent=self)
			m.position=meteor.position+(random.uniform(-20,20),random.uniform(-20,20))
			
			angle=random.uniform(0,pi*2)
			dx,dy=cos(angle)*80,sin(angle)*80
			
			m.run_action(A.move_by(dx,dy,0.6,TIMING_EASE_OUT))
			m.run_action(A.sequence(A.scale_to(0,0.6),A.remove()))

			
	def spawn_item(self):
		
		for i in range(9):
			for j in range(9):
				meteor=Meteor(parent=self)
				meteor.position=(self.size.w-65-(j*80),self.size.h-160-(i*80))
				
				d=random.uniform(2.0,4.0)
				
				self.items.append(meteor)
				
	def shoot_laser(self):
				if len(self.lasers) >=3:
					return 
			
				laser=SpriteNode('spc:LaserGreen12',parent=self)
				laser.position=self.player.position + (0,30)
				laser.z_position = -1
		
				actions=[A.move_by(0,self.size.h,1.2*self.speed),A.remove()]
				laser.run_action(A.sequence(actions))
		
				self.lasers.append(laser)
		
				sound.play_effect('digital:Laser4')
				
if __name__=='__main__':
	run(GameScene(),PORTRAIT,show_fps=True)
