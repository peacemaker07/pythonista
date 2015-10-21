#coding: utf-8
from scene import *
# Play a short melody
import sound

class MyScene ( Scene ):
	def setup ( self):
		self.x = self.size.w * 0.5
		self.y = self.size.h * 0.5
		
		sound.set_volume(1)
		
		# 障害物のシーケンスを作成
		w = 110
		self.s_rect = []
		while(self.size.w > w):
			h = 110
			while(self.size.h > h ):
				self.s_rect.append(Rect( w, h, 40, 40 ))
				h += 160
			else:
				w += 160

	def draw ( self ):
		# 毎回、描画しないと通ったところに色が残ってしまう
		background(1, 1, 1)
		fill(1, 0, 0)
		g = gravity ()
		self.x += g.x * 100
		self.y += g.y * 100
		self.x = min ( self.size.w - 40, max( 0, self.x ))
		self.y = min ( self.size.h - 40, max( 0, self.y ))

		# 動く四角を描画
		image('_Image_1', self.x, self.y, 40, 40)
		m_rect = Rect( self.x, self.y, 40, 40 )

		# 障害物を描画
		fill(1, 1, 0)
		for s in self.s_rect:
			image('_Image_2', s.x, s.y, s.w, s.h );

		# あたり判定	
		for i, s in enumerate( self.s_rect ):
			if m_rect.intersects( s ):
				'''
				# あたった四角の色をかえる
				fill( 1, 0, 0 )
				rect( s.x, s.y, s.w, s.h )
				'''
				# あたった四角を消す
				del self.s_rect[i]
				# 音をだす
				sound.play_effect('Crashing')


		

run( MyScene())
