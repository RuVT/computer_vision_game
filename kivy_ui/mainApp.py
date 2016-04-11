from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.image import ImageData
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from SimpleCV import Camera, Display, HaarCascade, Color, Image
from SimpleCV.base import np
import cv2

from pygame.image import tostring

class ControlUI(Widget):
	# val = ListProperty([])
	cvImage = ObjectProperty();
	# showBinarie = BooleanProperty(False)
	ts = []
	bb = (100,100,100,100,)
	imgPG = None

	def update(self, dt):
		# if self.display.isNotDone():
		self.img = self.cam.getImage().flipHorizontal()
		buffer = tostring(self.img.getPGSurface(),'RGB',True)
		imdata = ImageData(self.img.width, self.img.height, 'rgb', buffer)
		tex = Texture.create_from_data(imdata)
		self.cvImage.texture = tex
		# down = self.display.leftButtonDownPosition()
		# up = self.display.leftButtonUpPosition()
		# if(up is not None and down is not None):
		# 	bb = self.display.pointsToBoundingBox(up, down)
		# 	print(bb)
		# 	self.img.drawRectangle(bb[0],bb[1],bb[2],bb[3])
		# lower = np.array((float(self.val[0]), float(self.val[1]), float(self.val[2])))
		# upper = np.array((float(self.val[3]), float(self.val[4]), float(self.val[5])))
		# self.ts = self.img.track(img=self.img, ts=self.ts, bb=self.bb)
		# if self.ts:
		# 	self.ts[-1].draw()
		# 	self.ts[-1].drawBB()
		# lower = np.array((64.,129.,159.))
		# upper = np.array((80., 250., 245.))
		# hsv = self.img.toHSV()
		# mask = cv2.inRange(hsv.getNumpy(), lower, upper)
		# img2 = Image(source=mask)
		# img2 = img2.erode(1)
		# img2 = img2.dilate(2)
		# blops = img2.findBlobs(minsize=50, maxsize=100,)
		# if blops:
		# 	for b in blops:
		# 		if b.isRectangle() and b.minRectWidth():
		# 			self.img.draw(b)
		# self.img.save(self.display)



class MainApp(App):
	size = (100,100)
	def build(self):
		control = ControlUI()
		control.cam = Camera()
		# control.display = Display()
		Clock.schedule_interval(control.update, 1.0/60.0)
		return control


if __name__ == '__main__':
    MainApp().run()