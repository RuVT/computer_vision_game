from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock

from SimpleCV import Camera, Display, HaarCascade, Color, Image
from SimpleCV.base import np
import cv2

class ControlUI(Widget):
	val = ListProperty([])
	showBinarie = BooleanProperty(False)
	ts = []
	bb = (100,100,100,100,)
	img0 = Image("2016-04-07-160947.jpg")
	hand = HaarCascade('haarcascade_hand2.xml')

	def update(self, dt):
		if self.display.isNotDone():
			self.img = self.cam.getImage().flipHorizontal()
			lower = np.array((float(self.val[0]), float(self.val[1]), float(self.val[2])))
			upper = np.array((float(self.val[3]), float(self.val[4]), float(self.val[5])))
			self.ts = self.img.track(img=self.img, ts=self.ts, bb=self.bb, lower=lower, upper=upper)
			if self.ts:
				self.ts[-1].draw()
				self.ts[-1].drawBB()
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
			self.img.save(self.display)



class MainApp(App):
	size = (100,100)
	def build(self):
		control = ControlUI()
		control.cam = Camera()
		control.display = Display()
		Clock.schedule_interval(control.update, 1.0/60.0)
		return control


if __name__ == '__main__':
    MainApp().run()