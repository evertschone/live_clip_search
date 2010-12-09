import re

from callback_server import CallbackServer

LEN_CLIP_MSG = 6
CLIP_NAME_IDX = 4
TRACK_IDX = 2
CLIP_IDX = 3

class LiveClipSearchServer(CallbackServer):
    def __init__(self, logger, server_host = 'localhost', server_port = 9001, 
                 client_host = 'localhost', client_port = 9000):
        
        super(LiveClipSearchServer, self).__init__(logger,
                                                   server_host, server_port,
                                                   client_host, client_port)
        
        self._callback_manager.add(self._callback_view_clip, '/live/clip/view')
        self._callback_manager.add(self._callback_name_clip, '/live/name/clip')
        self._callback_manager.add(self._callback_play_clip, '/live/play/clip')
                
        self._clips = []
        
        self.get_clip_names()
    
    def _callback_name_clip(self, message = None):  
        self._log.debug("%s\t%s" % ("/live/name/clip", message))
        
        if len(message) == LEN_CLIP_MSG:
            clip_data = \
                (message[CLIP_NAME_IDX], message[TRACK_IDX], message[CLIP_IDX])
            self._clips.append(clip_data)
            
    def _callback_play_clip(self, message = None):
        self._log.debug("%s\t%s" % ("/live/play/clip", message))
        
    def _callback_view_clip(self, message = None):
        self._log.debug("%s\t%s" % ("/live/clip/view", message))
    
    def play_clip(self, track_idx, clip_idx):
        self._osc_client.send("/live/play/clip", (track_idx, clip_idx))   
    
    def search_clip_names(self, pattern):        
        match_names = [clip_data for clip_data in self._clips 
                       if re.search(pattern.lower(), clip_data[0].lower())]
        
        self._log.debug("%s\t%s" % ("match_names", match_names))    
        
        return sorted(match_names)
    
    def get_clip_names(self):
        self._osc_client.send("/live/name/clip")
