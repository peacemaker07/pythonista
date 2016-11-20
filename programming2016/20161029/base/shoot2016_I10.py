

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

