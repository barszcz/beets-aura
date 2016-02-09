
ERRORS = {
    'AudioFormatNotAcceptableError': {
        'message': 'Cannot transcode to audio format requested in Accept header',
        'status': 406
    }
}


class AudioFormatNotAcceptableError(Exception):
    '''Exception raised when the Accept headers of a request for an
    audio file stream do not match any type we can convert to'''

    def __init__(self, message, *args):
        super(AudioFormatNotAcceptableError,self).__init__(message, args)
        self.message = message
