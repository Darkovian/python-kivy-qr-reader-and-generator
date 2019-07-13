from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import StringProperty
# kivy.require("1.10.1")
import qrcode
from qrcode.image.pure import PymagingImage
import cv2
import zbar
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import os


class MenuScreen(Screen):
    pass


class ReadQR(Screen):

    def load(self, path, filename):
        loaded_code = cv2.imread(os.path.join(path, filename[0]), 0)
        scanner = zbar.Scanner()
        results = scanner.scan(loaded_code)
        for result in results:
            print(result.type, result.data, result.quality, result.position)
            byteData = result.data
            app = App.get_running_app()
            app.txtReadData = byteData.decode("UTF-8")


class DataScreen(Screen):
    pass


class GenerateQR(Screen):

    def genQR(self):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(self.ids["qr_data"].text)
        self.ids["qr_data"].text = ''
        qr.make(fit=True)
        if self.ids["checkBoxSave"].active:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y_[%H:%M:%S]")
            filename = timestampStr + ".png"
            save_img = qr.make_image(image_factory=PymagingImage)
            with open(filename, "wb") as saveStream:
                save_img.save(saveStream, "PNG")
        img = qr.make_image(fill_color="black", back_color="white")
        plt.imshow(img)
        plt.show()


class KivyQRApp(App):
    txtReadData = StringProperty()

    def build(self):
        self.sm = ScreenManager(transition=SwapTransition())
        self.menu = MenuScreen(name='menu')
        self.generate = GenerateQR(name='generate')
        self.read = ReadQR(name='read')
        self.dataread = DataScreen(name='datascreen')
        self.sm.add_widget(self.menu)
        self.sm.add_widget(self.generate)
        self.sm.add_widget(self.read)
        self.sm.add_widget(self.dataread)
        return self.sm

    def btnClose(self):
        sys.exit()

    def reloadFiles(self):
        self.sm.remove_widget(self.read)
        self.read = ReadQR(name='read')
        self.sm.add_widget(self.read)


if __name__ == "__main__":
    KivyQRApp().run()
