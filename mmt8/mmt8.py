# Alesis MMT-8 Simulator
# by Glenn Meader glenn@chromakinetics.com
# Micropython with LVGL v9
import tulip
from ui import UIElement, UILabel, lv, lv_depad
from UIButtonMatrix import UIButtonMatrix
from UILed import UILED
from mmt8_classes import Part, Track, Song
import json

        
mode='PART' 
edit_mode=False
loop = False
midi_echo = False   
tracks = [0]     
led_track =[0]    
bpm = 120
numbers=('0','1','2','3','4','5','6','7','8','9','+','-')


# init Parts and Songs & some test data
current_part = Part(0)
current_part.set_name('First part')
second_part = Part(1)
second_part.set_name('Second part')
current_song = Song(0)
current_song.set_name('My Song')
current_song.add_part(current_part)
current_song.add_part(second_part)
parts=[current_part,second_part]
songs=[current_song]

# callback fires when a button is clicked 
def button_matrix_cb(e):
    obj = e.get_target_obj() # obj that fired the event 
    code = e.get_code() # what type of event

    if code == lv.EVENT.VALUE_CHANGED:
        button_id = obj.get_selected_button()
        button_text = obj.get_button_text(button_id)
        #print('Changed BUTTON:',button_id,'TEXT:',button_text)
        cmd = button_text.split()
        
        if cmd[0] == 'PART':
            do_part()
        elif cmd[0] == 'SONG':
            do_song()
        elif cmd[0] == 'EDIT':
            do_edit()
        elif cmd[0] == '<<':
            do_rew()
        elif cmd[0] == '>>':
            do_fwd()
        elif cmd[0] in numbers: 
            do_number(cmd[0])

        elif cmd[0] == 'QUANT':
            do_quant()
        elif cmd[0] == 'COPY':
            do_copy()
        elif cmd[0] == 'TRANS':
            do_trans()
        elif cmd[0] == 'ERASE':
            do_erase()
        elif cmd[0] == 'LENGTH':
            do_length()
        elif cmd[0] == 'NAME':
            do_name()
        elif cmd[0] == 'MERGE':
            do_merge()
        elif cmd[0] == 'TAPE':
            do_tape()
        elif cmd[0] == 'MIDI' and cmd[1] == 'CHAN':
            do_chan()
        elif cmd[0] == 'PAGE': 
            do_page(cmd[1])  
        elif cmd[0] == 'PLAY':
            do_play()
        elif cmd[0] == 'RECORD':
            do_record()
        elif cmd[0] == 'STOP':
            do_stop()
        elif cmd[0] == 'LOOP':
            do_loop()
        elif cmd[0] == 'CLOCK':
            do_clock()
        elif cmd[0] == 'CLICK':
            do_click()
        elif cmd[0] == 'TEMPO':
            do_tempo()
        elif cmd[0] == 'MIDI' and cmd[1] == 'ECHO':
            do_echo()
        elif cmd[0] == 'MIDI' and cmd[1] == 'CHAN':
            do_chan()
        elif cmd[0] == 'MIDI' and cmd[1] == 'FILTER':
            do_filter()
        elif cmd[0] == 'TRACK':
            display_label.label.set_text('TRACK '+cmd[1])
            do_track(cmd[1]) 
        else:      
            display_label.label.set_text(button_text)



# create the command display label               
display_label = tulip.UILabel(text="* ALESIS MMT-8 *\n* VERSION 1.10 *", fg_color=tulip.color(255,255,0), font=tulip.lv.font_unscii_16)
display_label.label.set_height(60)
display_label.label.set_width(370)

# create a style for this Label
label_style = lv.style_t()
label_style.init()
label_style.set_bg_opa(lv.OPA.COVER) # need to do this opacity so bg_color will show
label_style.set_bg_color(lv.color_hex3(0x333)) 
label_style.set_text_color(lv.color_hex3(0xFF0))
label_style.set_border_color(lv.color_hex3(0xF0F))
label_style.set_border_width(1)
label_style.set_pad_top(2)
label_style.set_pad_bottom(10)
label_style.set_pad_right(6)
label_style.set_pad_left(6)
display_label.label.add_style(label_style, lv.PART.MAIN)

title_label = tulip.UILabel(text='MMT-8', fg_color=tulip.color(0,255,0), font=tulip.lv.font_montserrat_24)


# create LED objects
for t in range(1,9):
    led_track.insert(t, UILED(color=lv.color_hex3(0xF00)))
    tracks.insert(t,True)

led_loop = UILED(color=lv.color_hex3(0xF00))
led_echo = UILED(color=lv.color_hex3(0xF00))
led_part = UILED(color=lv.color_hex3(0xF00))
led_edit = UILED(color=lv.color_hex3(0xF00))
led_song = UILED(color=lv.color_hex3(0xF00))
led_play = UILED(color=lv.color_hex3(0xF00))
led_record = UILED(color=lv.color_hex3(0xF00))

# create button matrixes
left_commands_map =['QUANT','LENGTH','PART',"\n",
'COPY','NAME','EDIT',"\n",
'TRANS','MERGE','SONG',"\n",
'ERASE','TAPE','MIDI CHAN',"\n",
'PAGE DOWN','PAGE UP','']
numbers_map =['1','2','3','4','5',"\n",
                  '6','7','8','9','0',"\n",
                  '-','+','']
right_commands_map = [
'LOOP',"\n",
'MIDI ECHO',"\n",
'MIDI Filter',"\n",
'CLOCK',"\n",
'CLICK',"\n",
'TEMPO','']
tracks_map =['TRACK 1','TRACK 2','TRACK 3','TRACK 4','TRACK 5','TRACK 6','TRACK 7','TRACK 8','']
transport_map = ['<<','>>','PLAY', 'STOP / CONTINUE','RECORD','']
                  
left_button_matrix = UIButtonMatrix(left_commands_map, button_matrix_cb, h=330, width=300, fg_color=lv.color_hex3(0x000),
    bg_color=lv.color_hex3(0x556), button_bg_color=lv.color_hex3(0x999) )
numbers_button_matrix = UIButtonMatrix(numbers_map, button_matrix_cb, h=200, width=368, fg_color=lv.color_hex3(0x000),bg_color=lv.color_hex3(0x556), button_bg_color=lv.color_hex3(0x999) )
right_button_matrix = UIButtonMatrix(right_commands_map, button_matrix_cb, h=330, width=180, fg_color=lv.color_hex3(0x000),bg_color=lv.color_hex3(0x556), button_bg_color=lv.color_hex3(0x999) )
tracks_button_matrix = UIButtonMatrix(tracks_map, button_matrix_cb, h=80, width=900, fg_color=lv.color_hex3(0x000),bg_color=lv.color_hex3(0x556), button_bg_color=lv.color_hex3(0x999) )
transport_button_matrix = UIButtonMatrix(transport_map, button_matrix_cb, h=80, width=900, fg_color=lv.color_hex3(0x000),bg_color=lv.color_hex3(0x556), button_bg_color=lv.color_hex3(0x999) )

def do_page(direction):
    if direction=='UP':
        display_label.label.set_text('PAGE UP')
    else:
        display_label.label.set_text('PAGE DOWN')

def do_quant():
    display_label.label.set_text('QUANTIZE to 1/16\nNOTE START')

def do_copy():
    if mode=='SONG':
        display_label.label.set_text('COPY FROM SONG  '+str(current_song.number))
    if mode=='PART':
        display_label.label.set_text('COPY FROM PART  '+str(current_part.number))

def do_trans():
    display_label.label.set_text('TRANSPOSE UP\n00 SEMITONES')

def do_tempo():
    display_label.label.set_text('TEMPO = '+str(bpm)+'\nBEATS PER MINUTE')

def do_erase():
    if mode=='SONG':
        display_label.label.set_text('ERASE SONG  '+str(current_song.number))
    if mode=='PART':
        display_label.label.set_text('ERASE PART  '+str(current_part.number))

def do_length():
    display_label.label.set_text('PART '+ str(current_part.number)+"\nLENGTH 000 BEATS")

def do_name():
    if mode=='SONG':
        display_label.label.set_text('NAME SONG  '+str(current_song.number))
    if mode=='PART':
        display_label.label.set_text('NAME PART '+str(current_song.number)+"\n* NO PART NAME *")

def do_merge():
    display_label.label.set_text('SELECT 2 TRACKS\nTO BE MERGED')

def do_tape():
    display_label.label.set_text('SAVE ALL PARTS &\n SONGS TO TAPE') 
    print('MMT-8 dump')
    print('SONGS:')
    for (i,item) in enumerate(songs):
        print(item.number, item, item.name)
        for (p,part) in enumerate(item.parts):
            print('  ',part.number, part, part.name)
    #print(json.dumps(songs))

    print('PARTS:')
    for (i,item) in enumerate(parts):
        print(i, item, item.number, item.name)
    #print(json.dumps(parts))

    # page up/page down RECORD to Start 

def do_clock():
    display_label.label.set_text('CLOCK SOURCE:\nMIDI & INTERNAL') 

def do_click():
    display_label.label.set_text('CLICK VALUE 1/16:\nRECORD CLICK ON') 
    # numbers +- and pageup/down      

def do_filter():
    display_label.label.set_text('RECORD MIDI\nNOTES:     ON')  

def do_chan():
    display_label.label.set_text('SET MIDI CHANNEL\n  UNCHANGED') 

def do_part():
    global mode
    mode = 'PART'
    led_part.set_on()
    led_edit.set_off()
    led_song.set_off()
    display_label.label.set_text(' SELECT PART 00 \n* NO PART NAME *')

def do_song():  
    global mode
    mode = 'SONG'
    led_part.set_off()
    led_edit.set_off()
    led_song.set_on()  
    display_label.label.set_text(' SELECT SONG 00 \n* NO SONG NAME *')

def do_edit():  
    global mode
    led_edit.set_on()
    edit_mode=True
    if mode=='SONG':
        display_label.label.set_text('EDIT SONG  '+str(current_song.number))
    if mode=='PART':
        display_label.label.set_text('001/00: C#-2 064\n002/09  CHAN 01 ')

def do_number(num):
    display_label.label.set_text('NUMBER: '+ num)

def do_rew():
    display_label.label.set_text('REWIND')

def do_fwd():
    display_label.label.set_text('FAST FORWARD ')

def do_play():  
    global mode
    mode = 'PLAY'
    led_play.set_on()
    display_label.label.set_text('PLAYING PART '+ str(current_part.number)+"\n"+'BEAT 001')

def do_record():  
    global mode
    mode = 'RECORD'
    led_record.set_on()
    display_label.label.set_text('RECORD')

def do_stop():  
    global mode
    if mode== 'STOP':
        do_play() # continue
    else:
        mode = 'STOP'
        led_record.set_off()
        led_play.set_off()
        display_label.label.set_text('STOP')

def do_echo():  
    global midi_echo
    if midi_echo:
        led_echo.set_off()
        midi_echo = False
    else:
        led_echo.set_on()
        midi_echo = True
    display_label.label.set_text('MIDI ECHO '+str(midi_echo))

def do_loop():  
    global loop
    if loop:
        led_loop.set_off()
        loop = False
    else:
        led_loop.set_on()
        loop = True
    display_label.label.set_text('LOOP '+ str(loop))

def do_track(track_num):
    global tracks
    t=int(track_num)
    if tracks[t]:
        led_track[t].set_off()
        tracks[t] = False
    else:
        led_track[t].set_on()
        tracks[t] = True
    display_label.label.set_text('TRACK: ' + str(track_num)+' '+str(tracks[t]))
    
#set initial states   
led_play.set_off()
led_record.set_off()
led_loop.set_off()
led_echo.set_off()
led_edit.set_off()
led_song.set_off()
for t in range(1,9):
    led_track[t].set_off()
    tracks[t] = False

# start the app
def run(screen):
    screen.add(title_label, x=460, y=1, pad_x=250)
    screen.add(left_button_matrix,pad_x=200,x=10, y=20) 
    # put these here so that the led backgrounds get overlaid by the right_button Matrix - still dont know why LEDs have a wide black background
    screen.add(led_part, x=316, y=82)
    screen.add(led_edit, x=316, y=140)
    screen.add(led_song, x=316, y=200)
    screen.add(display_label, x=350, y=50, pad_x=250)
    screen.add(numbers_button_matrix,pad_x=260, x=335, y=120) 
    screen.add(right_button_matrix,pad_x=150, x=730, y=20) 
    screen.add(tracks_button_matrix,pad_x=900, x=10, y=380) 
    screen.add(transport_button_matrix,pad_x=900, x=10, y=480) 
    screen.add(led_track[1], x=95, y=393)
    screen.add(led_track[2], x=209, y=393)
    screen.add(led_track[3], x=318, y=393)
    screen.add(led_track[4], x=426, y=393)
    screen.add(led_track[5], x=530, y=393)
    screen.add(led_track[6], x=636, y=393)
    screen.add(led_track[7], x=744, y=393)
    screen.add(led_track[8], x=854, y=393)
    screen.add(led_loop, x=916, y=76)
    screen.add(led_echo, x=916, y=129)
    screen.add(led_play, x=478, y=494)
    screen.add(led_record, x=822, y=494)

    screen.present()
