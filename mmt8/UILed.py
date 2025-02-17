#  UI LED for tulip LVGL v 9.0

import tulip
from ui import UIElement, lv, lv_depad

class UILED(UIElement):

    def __init__(self,  h=None, width=None, fg_color=None, color=None, state=True, brightness=255, **kwargs):
        super().__init__(**kwargs)
        print(**kwargs)
        
        # create the buttonmatrix object
        self.led = lv.led(self.group)
        self.led.set_size(8,8)
        lv_depad(self.led)
        lv_depad(self.group)
        self.led.set_style_pad_all(lv.PART.MAIN,-3)
        self.led.set_style_pad_right(lv.PART.MAIN,0)

        # self.led.set_style_bg_color(lv.palette_main(lv.PALETTE.GREEN), 0)
        # self.led.set_style_bg_opa(lv.OPA._20,0) # opacity? creates s dark spot in the middle of the LED

        if(color is not None):
            self.led.set_color(color)  
        else:
            self.led.set_color(pal_to_lv(224))

        if(state):
            self.led.on()
        else:
            self.led.off()

        if(brightness is not None):
            self.led.set_brightness(brightness) 

    def hello(self):
        print('Hello LED')

    def set_off(self):
        self.led.off()
        #self.led.set_color(pal_to_lv(0))

    def set_on(self):
        self.led.on()
        #self.led.set_color(pal_to_lv(224))



