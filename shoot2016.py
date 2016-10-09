# coding: utf-8

from scene import *
import sound
import random
import time
from math import sin, cos, pi

A = Action

standing_texture = Texture('plf:AlienGreen_front')
walk_textures = [Texture('plf:AlienGreen_walk1'), Texture('plf:AlienGreen_walk2')]

game_duration = 10
disp_end_duration = 5

# 障害物
class Meteor (SpriteNode):
	def __init__(self, **kwargs):
		img = random.choice(['spc:MeteorBrownBig1', 'spc:MeteorBrownBig2'])
		SpriteNode.__init__(self, img, **kwargs)
		self.destroyed = False

class GameScene (Scene):
	
	# 初期設定		
	def setup(self):
		
		ground = Node(parent=self)
		
		# プレイヤーを配置
		self.player = SpriteNode(standing_texture)
		self.player.anchor_point = (0.5, 0)
		self.add_child(self.player)
		
		# スコアを配置
		score_font = ('Futura', 40)
		self.score_label = LabelNode('0', score_font, parent=self)
		self.score_label.position = (self.size.w/2, self.size.h - 70)
		self.score_label.z_position = 5
		
		# 制限時間を配置
		time_font = ('Futura', 40)
		self.time_label = LabelNode('00:00', time_font, parent=self)
		self.time_label.position = (self.size.w/3, self.size.h - 70)
		self.time_label.z_position = 5

		self.items = []
		self.lasers = []				
		
		self.new_game()
	
	def new_game(self):
		for item in self.items:
			item.remove_from_parent()
		
		# 背景色
		self.background_color = '#004f82'
								
		self.items = []
		self.lasers = []
		
		self.score = 0
		self.score_label.text = '0'
		
		self.start_time = time.time()
		
		self.walk_step = -1
		
		self.player.position = (self.size.w/2, 32)
		self.player.texture = standing_texture
		self.speed = 1.0
		
		self.game_over = False
		self.disp_end_time = disp_end_duration
				
		self.spawn_item()
	
	def update(self):
		if self.game_over:
			# ゲーム完了後、一定時間は完了画面を表示する
			time_passed = time.time() - self.disp_start_time
			self.disp_end_time = max(0, int(disp_end_duration - time_passed))
			self.time_label.text = '{0}:{1:0>2}'.format(self.disp_end_time/60, self.disp_end_time%60)
			return

		# プレイヤーの動きを更新
		self.update_player()
		# レーザーと障害物の衝突チェック
		self.check_laser_collisions()
		# 制限時間を更新
		time_passed = time.time() - self.start_time
		t = max(0, int(game_duration - time_passed))
		self.time_label.text = '{0}:{1:0>2}'.format(t/60, t%60)
		# タイムアップかチェックする
		if t == 0 and not self.game_over:
			self.disp_end_game('NG')
		
	def touch_began(self, touch):
		if self.game_over:
			if self.disp_end_time == 0:
				self.end_label.remove_from_parent()
				self.new_game()
		else:
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
		
	def check_laser_collisions(self):
		for laser in list(self.lasers):
			if not laser.parent:
				self.lasers.remove(laser)
				continue
			for item in self.items:
				if not isinstance(item, Meteor):
					continue
				if laser.position in item.frame:
					self.lasers.remove(laser)
					laser.remove_from_parent()
					self.destroy_meteor(item)
					break
	
	def destroy_meteor(self, meteor):
		sound.play_effect('arcade:Explosion_2', 0.2)
		
		meteor.remove_from_parent()
		self.items.remove(meteor)
		
		self.score += 10
		self.score_label.text = str(self.score)
		
		for i in xrange(5):
			m = SpriteNode('spc:MeteorBrownMed1', parent=self)
			m.position = meteor.position + (random.uniform(-20, 20), random.uniform(-20, 20))
			
			angle = random.uniform(0, pi*2)
			dx, dy = cos(angle) * 80, sin(angle) * 80
			
			m.run_action(A.move_by(dx, dy, 0.6, TIMING_EASE_OUT))
			m.run_action(A.sequence(A.scale_to(0, 0.6), A.remove()))
			
		self.check_end_game()
			
	def check_end_game(self):
		if len(self.items) == 0:
			self.disp_end_game('OK')
	
	def disp_end_game(self, status):
		
		if status == 'OK':
			message = 'Game Clear'
			color = '#00ff00'
			background_color = '#ffff00'
			effect = 'arcade:Powerup_1'
		else:
			message = 'Time Up'
			color = '#ff0000'
			background_color = '#000000'
			effect = 'arcade:Explosion_1'
		
		end_font = ('Arial Rounded MT Bold', 80)
		self.end_label = LabelNode(message, end_font, parent=self)
		self.end_label.position = (self.size.w/2, self.size.h - 300)
		self.end_label.z_position = 1
		self.end_label.color = color
		self.background_color = background_color
		
		self.game_over = True
		self.disp_start_time = time.time()
		
		sound.play_effect(effect)
			
	def spawn_item(self):
		for i in range(1):
			for j in range(9):
				meteor = Meteor(parent=self)
				meteor.position = (self.size.w-65-(j*80), self.size.h - 160 - (i*80))
				
				d = random.uniform(2.0, 4.0)
				
				self.items.append(meteor)
			
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
			
