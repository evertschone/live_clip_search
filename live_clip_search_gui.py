import tkFont

from threading import Thread
from Tkinter import *

LIST_SEP_SIZE = 8
WINDOW_TITLE = "Ableton Live Clip Search"
FONT_FAMILY = "FixedSys"

class LiveClipSearchGui(Thread):

    def __init__(self, logger, callback_find = None, callback_play = None,
                 callback_quit = None):
        Thread.__init__(self)        
          
        self._callback_find = callback_find  
        self._callback_play = callback_play
        self._callback_quit = callback_quit
        
        self._clip_names = []
        
        self._log = logger
        
        self._root_frame = Tk()
        
        self._setup_gui()
    
    def set_clip_names(self, clip_names):
        self._clip_name_list.delete(0, END)
        self._clip_names = []
        for clip_name, track_idx, clip_idx  in clip_names:
            self._clip_names.append((clip_name, track_idx, clip_idx))
            clip_info = self._format_list_entry(clip_name, track_idx, clip_idx)
            self._clip_name_list.insert(END, clip_info)
    
    def run(self):
        if self._root_frame:
            self._root_frame.mainloop()
            
    def _format_list_entry(self, clip_name, track_idx, clip_idx):
        return "  %d%s%d%s%s" % \
                (track_idx, " "*(LIST_SEP_SIZE - len(str(track_idx))),
                 clip_idx, " "*(LIST_SEP_SIZE - len(str(clip_idx))),
                 clip_name)
    
    def _play(self, row = None):
        if len(self._clip_names) == 0:
            return
        
        selected_idx = int(self._clip_name_list.curselection()[0])
        clip_name, track_idx, clip_idx = self._clip_names[selected_idx]
        self._callback_play(track_idx, clip_idx)
            
    def _find(self, event = None):
        query = self._name_entry.get()
        
        if len(query) == 0:
            self._clip_name_list.delete(0, END)
        else:
            self._callback_find(query)
        
    def _quit(self):
        for frame in [self._top_frame, self._mid_frame, self._bottom_frame]:
            frame.quit()
                    
        if self._callback_quit:
            self._callback_quit()
        
    def _setup_gui(self):
        self._root_frame.protocol("WM_DELETE_WINDOW", self._quit)
        self._root_frame.title(WINDOW_TITLE)
        
        font = tkFont.Font(root = self._root_frame, family = FONT_FAMILY, 
                           size=14)
        
        self._top_frame = Frame(self._root_frame)
        self._top_frame.pack(fill = X, padx = 10, pady = 10)
        
        self._mid_frame = Frame(self._root_frame)
        self._mid_frame.pack(fill = X, padx = 10)
        
        self._bottom_frame = Frame(self._root_frame)
        self._bottom_frame.pack(fill = BOTH, expand = 1, padx = 10, pady = 5)
                
        self._pattern_label = Label(self._top_frame, font = font, 
                                    text = "Pattern:  ")
        self._pattern_label.pack(side = LEFT)
        
        track_title = "Track    " 
        self._track_label = Label(self._mid_frame, font = font, 
                                  text = track_title)
        self._track_label.pack(side = LEFT)
        
        clip_title = "Clip    " 
        self._clip_label = Label(self._mid_frame, font = font, 
                                 text = clip_title)
        self._clip_label.pack(side = LEFT)
        
        clip_title = "Name" 
        self._name_label = Label(self._mid_frame, font = font, text = "Name")
        self._name_label.pack(side = LEFT)
        
        self._name_entry = Entry(self._top_frame, font = font)
        self._name_entry.pack(fill = X)
        self._name_entry.bind("<KeyRelease>", self._find)
        
        #self._find_button = Button(self._mid_frame, text = "Find", 
        #                           command=self._find)
        #self._find_button.pack(fill = X)
        
        self._y_scroll = Scrollbar(self._bottom_frame)
        self._y_scroll.pack(side = RIGHT, fill = Y)
        
        self._clip_name_list = Listbox(self._bottom_frame, width = 100, 
                                       height = 30, font = font)
        self._clip_name_list.configure(yscrollcommand = self._y_scroll.set)
        self._clip_name_list.bind("<Double-Button-1>", self._play)
        self._clip_name_list.pack(fill = BOTH, expand = 1)
        
        self._y_scroll.config(command=self._clip_name_list.yview)
        
        #self._play_button = Button(self._bottom_frame, text = "PLAY", 
        #                           fg = "green", command = self._play)
        #self._play_button.pack(fill = X)
        
        #self._quit_button = Button(self._bottom_frame, text = "QUIT", 
        #                           fg = "red", command=self._quit)
        #self._quit_button.pack(fill = X)