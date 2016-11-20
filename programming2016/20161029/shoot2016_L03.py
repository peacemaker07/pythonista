# coding: utf-8

from scene import *
import sound
import random

A = Action

# プレイヤーの画像
standing_texture = Texture('plf:AlienBeige_front')
walk_textures = [Texture('plf:AlienBeige_climb1'), Texture('plf:AlienBeige_climb2')]

# 障害物
class Meteor (SpriteNode):
	def __init__(self, **kwargs):
		img = random.choice(['plf:Tile_BrickBrown', 'plf:Tile_BrickGrey'])
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

		# 障害物のリストを初期化
		self.items = []
		# 弾のリストを初期化
		self.lasers = []				
		
		# 新しいゲームの準備
		self.new_game()
	
	def new_game(self):
		# 背景色
		self.background_color = '#004f82'
		
		self.items = []
		self.lasers = []
		
		# プレイヤーを立っている状態に設定
		self.walk_step = -1
		# プレイヤーを配置
		self.player.position = (self.size.w/2, 10)
		self.player.texture = standing_texture
		self.speed = 1.0
		
		# 障害物を配置
		self.spawn_item()
	
	def update(self):
		# プレイヤーの動きを更新
		self.update_player()
		# レーザーと障害物の当たりチェック
		self.check_laser_collisions()
		
	def touch_began(self, touch):
		# 弾をだす
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
			# 画面外にある弾を削除
			if not laser.parent:
				self.lasers.remove(laser)
				continue

	def spawn_item(self):
		# 障害物を配置
		for i in range(9):
			for j in range(9):
				meteor = Meteor(parent=self)
				meteor.position = (self.size.w-65-(j*80), self.size.h - 160 - (i*80))
				
				d = random.uniform(2.0, 4.0)
				
				self.items.append(meteor)

	def shoot_laser(self):
		if len(self.lasers) >= 3:
			return
		
		# 弾を描画
		laser = SpriteNode('spc:LaserGreen12', parent=self)
		laser.position = self.player.position + (0, 30)
		laser.z_position = -1
		
		actions = [A.move_by(0, self.size.h, 1.2 * self.speed), A.remove()]
		laser.run_action(A.sequence(actions))
		
		self.lasers.append(laser)
		
		# 発射音を鳴らす
		sound.play_effect('digital:Laser4')

if __name__ == '__main__':
	run(GameScene(), PORTRAIT, show_fps=True)
