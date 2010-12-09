import logging

from live_clip_search_gui import LiveClipSearchGui
from live_clip_search_server import LiveClipSearchServer

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

class LiveClipSearch:
    def __init__(self):
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(LOG_FORMAT))
        self._log = logging.getLogger()
        self._log.addHandler(ch)
        self._log.setLevel(LOG_LEVEL)
        
        self._gui_thread = LiveClipSearchGui(self._log, self._callback_find,
                                             self._callback_play, 
                                             self._callback_quit)
        
        self._server_thread = LiveClipSearchServer(self._log)
    
    def run_threads(self):
        self._gui_thread.start()
        self._server_thread.start()
        
        self._gui_thread.join()
        self._server_thread.join()
        
    def _callback_quit(self):
        self._server_thread.quit()
    
    def _callback_find(self, pattern):
        match_names = self._server_thread.search_clip_names(pattern)
        self._gui_thread.set_clip_names(match_names)
    
    def _callback_play(self, track_idx, clip_idx):
        self._server_thread.play_clip(track_idx, clip_idx)
    
if __name__ == "__main__":
    live_clip_search = LiveClipSearch()
    live_clip_search.run_threads()