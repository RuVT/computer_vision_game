from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.image import ImageData
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import Color as kvColor, Ellipse, Line
from kivy.lang import Builder

from SimpleCV import Camera, Display, HaarCascade, Color, Image
from SimpleCV.base import np
import cv2

from pygame.image import tostring

import numpy

def getKivyTexture(img):
	buffer = tostring(img.getPGSurface(),'RGB',True)
	# buffer = img.toString()
	imdata = ImageData(img.width, img.height, 'rgb', buffer)
	tex = Texture.create_from_data(imdata)
	return tex

Builder.load_file("menuScreen.kv")
Builder.load_file("configScreen.kv")
Builder.load_file("gameScreen.kv")


class GameInstance:
	instance = None

	class __GameInstance:
		lower = np.array((float(0), float(0), float(0)))
		upper = np.array((float(0), float(0), float(0)))

		def __init__(self):
			self.cam = Camera()

	def __init__(self):
		if(GameInstance.instance is None):
			GameInstance.instance = GameInstance.__GameInstance()

	def __getattr__(self, name):
		return getattr(self.instance, name)

	def __setattr__(self, name, value):
		setattr(self.instance, name, value)


class CommonScreen:
	blob_coor = ListProperty([0,0])

	def init(self):
		Clock.schedule_interval(self.update, 1.0/60.0)

	def end(self):
		Clock.unschedule(self.update)


class GameScreen(Screen,CommonScreen):
	game = ObjectProperty()
	last_pos = [None, None]
	limit_dist = 30.

	def movement_filter(self, pos):
		if self.last_pos[0] is None:
			self.last_pos[0] = pos
		else:
			dist = numpy.linalg.norm(pos-self.last_pos[0])
			if dist < self.limit_dist:
				self.last_pos[1] = pos

	def update(self, dt):
		self.img = GameInstance().cam.getImage().flipHorizontal()
		hsv = self.img.toHSV()
		mask = cv2.inRange(hsv.getNumpy(), GameInstance().lower, GameInstance().upper)
		img2 = Image(source=mask)
		img2 = img2.erode(1)
		img2 = img2.dilate(2)
		blops = img2.findBlobs()
		if blops:
			largest = blops[-1]
			x, y = largest.centroid()
			y = self.size[1]-y
			self.movement_filter(numpy.array([x, y]))
			self.blob_coor[0] = x
			self.blob_coor[1] = y
			if self.last_pos[1] is not None:
				with self.game.canvas:
					kvColor(1, 1, 0)
					d = 10.
					# Ellipse(pos=(x - d / 2, self.blob_coor[1] - d / 2), size=(d, d))
					Line(points=(self.last_pos[0][0], self.last_pos[0][1],self.last_pos[1][0], self.last_pos[1][1]))
					self.last_pos[0] = self.last_pos[1]

	def clear(self):
		self.game.canvas.clear()
		self.last_pos = [None, None]


class MenuScreen(Screen):
	pass


class ConfigScreen(Screen,CommonScreen):
	val = ListProperty([])
	cvImage = ObjectProperty()
	cvFilter = ObjectProperty()
	cvBlob = ObjectProperty()
	cvActiveBloops = ObjectProperty()

	def update(self, dt):
		self.img = GameInstance().cam.getImage().flipHorizontal()
		GameInstance().lower = np.array((float(self.val[0]), float(self.val[1]), float(self.val[2])))
		GameInstance().upper = np.array((float(self.val[3]), float(self.val[4]), float(self.val[5])))
		hsv = self.img.toHSV()
		mask = cv2.inRange(hsv.getNumpy(), GameInstance().lower, GameInstance().upper)
		img2 = Image(source=mask)
		img2 = img2.erode(1)
		img2 = img2.dilate(2)
		if self.cvActiveBloops.active:
			blops = img2.findBlobs()
			if blops:
				self.cvBlob.texture = getKivyTexture(blops[-1].getMaskedImage())
		self.cvFilter.texture = getKivyTexture(img2)
		self.cvImage.texture = getKivyTexture(self.img)


class MainApp(App):
	def build(self):
		root = ScreenManager()
		root.add_widget(MenuScreen(name="Menu"))
		root.add_widget(ConfigScreen(name="Configuration"))
		root.add_widget(GameScreen(name="Game"))
		return root


if __name__ == '__main__':
    MainApp().run()