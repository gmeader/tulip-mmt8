#  UI button matrix for tulip LVGL v 9.0

import tulip
from ui import UIElement, lv, lv_depad

class UIButtonMatrix(UIElement):
    def __init__(self, map, callback, one_checked=True, h=None, width=None, fg_color=None, bg_color=None, button_bg_color=None, **kwargs):
        super().__init__(**kwargs)
        print(**kwargs)
        self.map = map
        # map is a list of button names/labels
        '''
        like this:
        button_map = ['1','2','3',"\n",
                  '4','5','6',"\n",
                  '7','8','9',"\n",
                  '0','Go','']
        Add command:
           screen.add(UIButtonMatrix(button_map, callback=cb_name), pad_x=150,x=20, y=20) # need to add pad_x or the container is clipped
        '''
        # create the buttonmatrix object
        self.bmatrix = lv.buttonmatrix(self.group)
        self.bmatrix.set_map(self.map)
        self.bmatrix.add_event_cb(callback,lv.EVENT.ALL, None)
        if(h is not None):
            self.bmatrix.set_height(h)  
        if(width is not None):
            self.bmatrix.set_width(width) 


        # style to color the buttons colors
        self.button_style = lv.style_t()
        self.button_style.init()
        if(button_bg_color is not None):
            self.button_style.set_bg_color(button_bg_color)
        if(fg_color is not None):
            self.button_style.set_text_color(fg_color)

        ### maybe can set local style without having to create a style? self.bmatrix.set_style_bg_color(bg_color, lv.PART.MAIN)
        # style to color the button matrix container background
        self.container_style = lv.style_t()
        self.container_style.init()
        if(bg_color is not None):
            self.container_style.set_bg_color(bg_color)

        # set some attributes of the buttonmatrix
        #self.bmatrix.set_button_ctrl_all(lv.buttonmatrix.CTRL.CHECKABLE) # make buttons toggle on/off
        #self.bmatrix.set_one_checked(one_checked) # default - only let one button be toggled on at a time
        # self.bmatrix.align(lv.ALIGN.CENTER,0,0) # maybe this is the default?

        # apply the styles for the buttons and for the container
        self.bmatrix.add_style(self.button_style, lv.PART.ITEMS)
        self.bmatrix.add_style(self.container_style, lv.PART.MAIN) 
        self.bmatrix.set_style_bg_color(lv.color_hex3(0x88F), lv.PART.ITEMS | lv.STATE.PRESSED)  # color when clicked                        
