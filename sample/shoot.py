# coding: utf-8

from scene import *
import sound
import random
from math import sin, cos, pi

A = Action

standing_texture = Texture('plf:AlienGreen_front')
walk_textures = [Texture('plf:AlienGreen_walk1'), Texture('plf:AlienGreen_walk2')]

hit_texture = Texture('plf:AlienGreen_hit')

# 
class Coin (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, 'plf:Item_CoinGold', **kwargs)

# 障害物
class Meteor (SpriteNode):
	def __init__(self, **kwargs):
		img = random.choice(['spc:MeteorBrownBig1', 'spc:MeteorBrownBig2'])
		SpriteNode.__init__(self, img, **kwargs)
		self.destroyed = False

class GameScene (Scene):
	
	# 初期設定		
	def setup(self):
		# 背景色
		self.background_color = '#004f82'
		
		ground = Node(parent=self)
		
		# プレイヤーを配置
		self.player = SpriteNode(standing_texture)
		self.player.anchor_point = (0.5, 0)
		self.add_child(self.player)
		
		# スコアを配置
		score_front = ('Futura', 40)
		self.score_label = LabelNode('0', score_front, parent=self)
		self.score_label.position = (self.size.w/2, self.size.h - 70)
		self.score_label.z_position = 1

		self.items = []
		self.lasers = []				
		
		self.new_game()
	
	def new_game(self):
		for item in self.items:
			item.remove_from_parent()
			
		self.items = []
		self.lasers = []
		
		self.score = 0
		self.score_label.text = '0'
		
		self.walk_step = -1
		
		self.player.position = (self.size.w/2, 32)
		self.player.texture = standing_texture
		self.speed = 1.0
		
		self.game_over = False
	
	def update(self):
		if self.game_over:
			return
		# プレイヤーの動きを更新
		self.update_player()
		# プレイヤーとコインの衝突チェック
		self.check_item_collisions()
		# レーザーと障害物の衝突チェック
		self.check_laser_collisions()
		
		if random.random() < 0.05:
			self.spawn_item()
			
	def touch_began(self, touch):
		self.shoot_laser()
	
	def update_player(self):
	
		g = gravity()
		if abs(g.x) > 0.05:
			self.player.x_scale = cmp(g.x, 0)
			x = self.player.position.x
			max_speed = 40
			x = max(0, min(self.size.w, x + g.x * max_speed))
			self.player.position = (x, 32)

			step = int(self.player.position.x / 40) % 2
			
			if step != self.walk_step:
				self.player.texture = walk_textures[step]
				
				sound.play_effect('rpg:Footstep00', 0.05, 1.0 + 0.5 * step)
				self.walk_step = step
		else:
			self.player.texture = standing_texture
			self.walk_step = -1

	def check_item_collisions(self):
		
		player_hitbox = Rect(self.player.position.x - 20, 32, 40, 65)
		
		for item in list(self.items):
			if item.frame.intersects(player_hitbox):
				if isinstance(item, Coin):
					self.collect_item(item)
				elif isinstance(item, Meteor):
					if item.destroyed:
						self.collect_item(item, 100)
					else:
						self.player_hit()
			elif not item.parent:
				self.items.remove(item)
	
	def check_laser_collisions(self):
		for laser in list(self.lasers):
			if not laser.parent:
				self.lasers.remove(laser)
				continue
			for item in self.items:
				if not isinstance(item, Meteor):
					continue
				if item.destroyed:
					continue
				if laser.position in item.frame:
					self.destroy_meteor(item)
					self.lasers.remove(laser)
					laser.remove_from_parent()
					break
	
	def check_laser_collisions(self):
		for laser in list(self.lasers):
			if not laser.parent:
				self.lasers.remove(laser)
				continue
			for item in self.items:
				if not isinstance(item, Meteor):
					continue
				if item.destroyed:
					continue
				if laser.position in item.frame:
					self.destroy_meteor(item)
					self.lasers.remove(laser)
					laser.remove_from_parent()
					break
	
	def destroy_meteor(self, meteor):
		sound.play_effect('arcade:Explosion_2', 0.2)
		meteor.destroyed = True
		meteor.texture = Texture('plf:Item_Star')
		
		for i in xrange(5):
			m = SpriteNode('spc:MeteorBrownMed1', parent=self)
			m.position = meteor.position + (random.uniform(-20, 20), random.uniform(-20, 20))
			
			angle = random.uniform(0, pi*2)
			dx, dy = cos(angle) * 80, sin(angle) * 80
			m.run_action(A.move_by(dx, dy, 0.6, TIMING_EASE_OUT))
			m.run_action(A.sequence(A.scale_to(0, 0.6), A.remove()))
	
	def player_hit(self):
		self.game_over = True
		sound.play_effect('arcade:Explosion_1')
		
		self.player.texture = hit_texture
		
		self.player.run_action(A.move_by(0, -150))
		
		self.run_action(A.sequence(A.wait(2*self.speed), A.call(self.new_game)))
	
	def spawn_item(self):
		if random.random() < 0.3:
			meteor = Meteor(parent=self)
			meteor.position = (random.uniform(20, self.size.w-20), self.size.h + 30)
			
			d = random.uniform(2.0, 4.0)
			
			actions = [A.move_to(random.uniform(0, self.size.w), -100, d), A.remove()]
			
			meteor.run_action(A.sequence(actions))
			self.items.append(meteor)
		else:
			coin = Coin(parent=self)
			coin.position= (random.uniform(20, self.size.w-20), self.size.h + 30)
			
			d = random.uniform(2.0, 4.0)
			
			actions = [A.move_by(0, -(self.size.h + 60), d), A.remove()]
			
			coin.run_action(A.sequence(actions))
			self.items.append(coin)
			
		self.seed = min(3, self.speed + 0.005)
		
	def collect_item(self, item, value=10):
		if value > 10:
			sound.play_effect('digital:PowerUp8')
		else:
			sound.play_effect('digital:PowerUp7')
			
		item.remove_from_parent()
		self.items.remove(item)
		
		self.score += value
		self.score_label.text = str(self.score)

	def shoot_laser(self):
		if len(self.lasers) >= 3:
			return
		
		laser = SpriteNode('spc:LaserGreen12', parent=self)
		laser.position = self.player.position + (0, 30)
		laser.z_position = -1
		
		actions = [A.move_by(0, self.size.h, 1.2 * self.speed), A.remove()]
		laser.run_action(A.sequence(actions))
		
		self.lasers.append(laser)
		sound.play_effect('digital:Laser4')

if __name__ == '__main__':
	run(GameScene(), PORTRAIT, show_fps=True)
			
