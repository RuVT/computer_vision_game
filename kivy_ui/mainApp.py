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

def getKivyTexture(img):
	buffer = tostring(img.getPGSurface(),'RGB',True)
	# buffer = img.toString()
	imdata = ImageData(img.width, img.height, 'rgb', buffer)
	tex = Texture.create_from_data(imdata)
	return tex


class ControlUI(Widget):
	val = ListProperty([])
	cvImage = ObjectProperty();
	cvFilter = ObjectProperty();
	cvActiveBloops = ObjectProperty();
	blop_coord = ObjectProperty();
	# showBinarie = BooleanProperty(False)
	ts = []
	bb = (100,100,100,100,)
	imgPG = None

	def update(self, dt):
		# if self.display.isNotDone():
		self.img = self.cam.getImage().flipHorizontal()
		self.img.drawRectangle(50,50,200,200)
		lower = np.array((float(self.val[0]), float(self.val[1]), float(self.val[2])))
		upper = np.array((float(self.val[3]), float(self.val[4]), float(self.val[5])))

		hsv = self.img.toHSV()
		mask = cv2.inRange(hsv.getNumpy(), lower, upper)
		img2 = Image(source=mask)
		img2 = img2.erode(1)
		img2 = img2.dilate(2)
		if self.cvActiveBloops.active:
			blops = img2.findBlobs(minsize=50, maxsize=200)
			if blops:
				for b in blops:
					if b.isRectangle():
						self.blop_coord.text = b.centroid()
		self.cvFilter.texture = getKivyTexture(img2)
		self.cvImage.texture = getKivyTexture(self.img)


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