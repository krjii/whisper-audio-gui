'''
Created on Nov 13, 2024

@author: kevinrjamesii
'''
import whisper


class AudioText(whisper.Whisper):
    '''
    classdocs
    '''


    def __init__(self, params=None):
        '''
        Constructor
        '''
        super().__init__()      
        # self.model = self whisper.load_model("turbo")        