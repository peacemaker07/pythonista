# coding: utf-8

from scene import *
import sound

A = Action

# プレイヤーの画像
standing_texture = Texture('plf:AlienBeige_front')
walk_textures = [Texture('plf:AlienBeige_climb1'), Texture('plf:AlienBeige_climb2')]

# 障害物の画像
meteor_img = ['plf:Tile_BrickBrown', 'plf:Tile_BrickGrey']



	def new_game(self):
		# 背景色
		self.background_color = '#004f82'
		
		self.items = []
		
		# プレイヤーを立っている状態に設定
		self.walk_step = -1
		# プレイヤーを配置
		self.player.position = (self.size.w/2, 10)
		self.player.texture = standing_texture
		self.speed = 1.0
		
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
