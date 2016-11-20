# -*- coding:utf-8 -*-
from scene import *
from threading import Timer
import sound

class GameScene(Scene):
	
	IMAGE_PLAYER = 'Coffee'
	IMAGE_ENEMY = 'Alien_Monster'
	IMAGE_BALL = 'Chestnut'
	
	SOUND_SHOT = 'Shot'
	SOUND_CRASH = 'Crashing'

	BALL_INIT_Y = 40
	BALL_MAX_X = 1024
	BALL_MAX_Y = 700

	def setup(self):

		# 初期化
		self.s_ball = [] # 弾の配列
		self.score = 0 # 点数
		self.gameover_tot = 20 # リミット時間
		self.gamestatus = 1 # ゲームステータス(1:ゲーム, 2:ゲームクリアー, 3:ゲームオーバー)

		# 基礎のレイヤーを作成
		self.root_layer = Layer(self.bounds)
		center = self.bounds.center()
		
		# ゲーム用のレイヤーを作成
		self.game_layer = Layer(self.bounds)
		self.game_layer.background = Color(1, 30, 100)
		self.root_layer.add_layer(self.game_layer)
		
		# プレイヤーを描画
		self.x = center.x - 64
		self.y = 20
		self.player = self.player_display(self.x, self.y)

		# インベーダーデータを作成
		w = 50
		self.s_rect = []
		while(self.size.w > w):
			h = 110
			while(self.size.h > h + 100):
				self.s_rect.append(Rect(w, h, 40, 40))
				h += 100
			else:
				w += 100
				
		# タイムアウトした際に呼ばれる関数を登録してタイマー開始
		self.timer_start()
		
	def draw(self):
		
		center = self.bounds.center()
		background(0, 0, 0)
		
		if self.gamestatus == 2: # ゲームクリアー
			self.proc_gameend()
			return # 処理終了
		elif self.gamestatus == 3: # ゲームオーバー
			self.proc_gameend()
			return # 処理終了
		
		# 点数を表示
		self.text_display()
		
		# プレイヤーを描画
		# 重力値から移動量を算出
		g = gravity()
		self.x += g.x * 100
		self.y = 20
		# 画面外へいかないように調整
		self.x = min(self.size.w - 100, max(0, self.x))
		self.y = min(self.size.h - 100, max(0, self.y))
		self.player = self.player_display(self.x, self.y)

		# あたり判定
		for i, b in enumerate(self.s_ball):
			for j, s in enumerate(self.s_rect):
				if b.intersects(s):
					# 当たった障害物と弾を消す
					del self.s_rect[j]
					del self.s_ball[i]
					# 音をだす
					sound.play_effect(self.SOUND_CRASH)
					# 点数を加算
					self.score += 10
			
		# 障害物を描画
		for s in self.s_rect:
			image(self.IMAGE_ENEMY, s.x, s.y, s.w, s.h);

		# 弾の描画
		for i, b in enumerate(self.s_ball):
			# プレイヤーの位置から弾のx位置を再度計算
			x = self.ball_x_position()
			y = b.y + 10
			# 画面外へいった場合は弾を削除
			if y >= self.BALL_MAX_Y:
				del self.s_ball[i]
			else:
				self.s_ball[i] = self.ball_display(x, y)
				
		# ゲームの終了判定
		if len(self.s_rect) == 0:
			self.timer.cancel()
			self.gamestatus = 2 # ゲームクリア
			self.create_gameend_layer()			

	def touch_began(self, touch):
		
		# ゲーム中でなければ何もしない
		if self.gamestatus != 1: return
		
		# 画面をタッチした際に呼ばれる関数
		center = self.bounds.center()
		
		# タッチした座標を保持
		x, y = touch.location.x, touch.location.y
		# 弾を作成
		self.s_ball.append(self.ball_display(self.ball_x_position(), self.BALL_INIT_Y))
		# 音をだす
		sound.play_effect(self.SOUND_SHOT)

	def callback_timer(self):
		# タイムアウトした際に呼ばれる関数
		self.gameover_tot = self.gameover_tot - 1
		if self.gameover_tot >= 0: # タイムアウトしていない
			self.timer_start()
		else:
			self.gamestatus = 3 # ゲームオーバー
			self.create_gameend_layer()

	def create_gameend_layer(self):
		# ゲーム終了画面作成
		self.root_layer.remove_layer(self.game_layer)
		self.gameend_layer = Layer(self.bounds)
		
		if self.gamestatus == 2: # ゲームクリアー
			self.gameend_layer.background = Color(200, 0, 100)
		elif self.gamestatus == 3: # ゲームオーバー
			self.gameend_layer.background = Color(200, 200, 0)
			
		self.root_layer.add_layer(self.gameend_layer)
		
	def proc_gameend(self):
		self.gameend_layer.update(self.dt)
		self.gameend_layer.draw()
		self.text_display()

	def timer_start(self):
		# タイムアウトした際に呼ばれる関数を登録してタイマー開始
		self.timer = Timer(1.0, self.callback_timer)
		self.timer.start()

	def text_display(self):
		w, h = self.size.w, self.size.h
		font = 'GillSans'
		h_x_pos = l_x_pos = w * 0.5
		
		if self.gamestatus == 1:
			h_text = u"スコア   ：" + str(self.score)
			h_size = 40
			h_y_pos = h - 30
		
			l_text = u"残り：" + str(self.gameover_tot) + u"秒  "
			l_size = 40
			l_y_pos = h - 70
		else:
			if self.gamestatus == 2:
				h_text = u"ゲームクリアー\＾o＾/"
			elif self.gamestatus == 3:
				h_text = u"ゲームオーバー orz..."
			
			h_size = 100
			h_y_pos = h - 300
			
			l_text = u"スコア   ：" + str(self.score)
			l_size = 40
			l_y_pos = h - 50
		
		# 点数を表示
		tint(1.0, 1.0, 1.0)
		text(h_text, font, h_size, h_x_pos, h_y_pos)

		# 残時間を表示
		tint(100.0, 100.0, 100.0)
		text(l_text, font, l_size, l_x_pos, l_y_pos)

	def player_display(self, x, y):
		# プレイヤーを描画して位置を返却する
		image(self.IMAGE_PLAYER, x, y, 100, 100)
		return Rect(x, y, 100, 100)		
	
	def ball_display(self, x, y):
		# 弾を描画して位置を返却する
		image(self.IMAGE_BALL, x, y, 32, 32)
		return Rect(x, y, 32, 32)
	
	def ball_x_position(self):
		# 弾のx座標を返却する
		return self.player.center().x - 16

run(GameScene())

