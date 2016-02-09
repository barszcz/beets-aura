
import os
import subprocess
import select
import errno
import logging

from .errors  import AudioFormatNotAcceptableError

# Values from FFMPEG documentation:
# https://trac.ffmpeg.org/wiki/Encode/MP3
def get_Vquality(samplerate):
    '''Return variable quality number for mp3 encoding
    such that actual samplerate will stay below parameter'''

    if samplerate <= 85:
        return 9
    elif samplerate <= 105:
        return 8
    elif samplerate <= 120:
        return 6
    elif samplerate <= 150:
        return 5
    elif samplerate <= 185:
        return 4
    elif samplerate <= 195:
        return 3
    elif samplerate <= 210:
        return 2
    elif samplerate <= 250:
        return 1
    else:
        return 0

def convert_ffmpeg(input_file, format, samplerate=None):
    '''Convert audio using generic ffmpeg command.'''
    convert_command = ["ffmpeg", "-i", input_file ]
    if format:
        convert_command.extend(["-f", format ])
    if samplerate:
        convert_command.extend(["-q:a", get_Vquality(samplerate)])
    convert_command.append("-")
    #print "converting with ffmpeg command: {}".format(convert_command)
    return subprocess.Popen(convert_command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)


def convert_sox(input_file,format,samplerate=None):
    '''Convert audio using generic sox command.'''
    convert_command = [ "sox", "-V0", input_file ]
    if format:
        convert_command.extend(['-t', format])
    if samplerate:
        convert_command.extend(['-r', samplerate])
    convert_command.append('-')
    logging.debug("converting with sox command: {}".format(convert_command))

    return subprocess.Popen(convert_command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

# From outputs of `sox --help` and `ffmpeg -encoders`
conversion_formats = \
    set(map(lambda f: '.'+f, """8svx aif aifc aiff aiffc al amb au avr caf cdda cdr cvs cvsd cvu \
    dat dvms f32 f4 f64 f8 fap flac fssd gsm gsrt hcom htk ima ircam la lu \
    mat mat4 mat5 maud nist ogg paf prc pvf raw s1 s16 s2 s24 s3 s32 s4 s8 \
    sb sd2 sds sf sl sln smp snd sndfile sndr sndt sou sox sph sw txw u1 \
    u16 u2 u24 u3 u32 u4 u8 ub ul uw vms voc vorbis vox w64 wav wavpcm \
    wv wve xa xi mp3""".split()))

# Screw you proprietary formats. All of you.
def convert(input_file, format, samplerate=None):
    if format.startswith('.'):
        format = format.lstrip('\.')
    #print "Format desired: {}".format(format)
    if format == "mp3":
        conv_fn = convert_ffmpeg
    else:
        conv_fn = convert_sox

    return conv_fn(input_file, format, samplerate)

def communicate_stream(proc, pipe_fd):
    '''Communicate with subprocess via generators for streaming interface
    rather than blocking via Popen.communicate().'''

    if pipe_fd not in [proc.stdout, proc.stderr]:
        return
    while True:
        try:
            rlist, wlist, xlist = select.select([pipe_fd],[],[])
        except select.error, e:
            if e.args[0] == errno.EINTR:
                continue
            raise

        if pipe_fd in rlist:
            data = os.read(pipe_fd.fileno(),1024)
            if proc.return_code is not None and proc.return_code != 0:
                raise AudioFormatNotAcceptableError()
            if data == "":
                pipe_fd.close()
                return
            yield data

def conversion_stream(track_file, format, samplerate=None):
    '''Convenience method to return both stderr and stdout streams.'''
    conv_proc = convert(track_file, format, samplerate)
    return (communicate_stream(conv_proc,conv_proc.stdout),
            communicate_stream(conv_proc,conv_proc.stderr))

def file_stream(audio_fn, seek=0):
    '''Stream file in chunks'''
    print 'Audio File: {}'.format(audio_fn)
    try:
        with open(audio_fn, 'rb') as af:
            while True:
                chunk = af.read(1024)
                if not chunk:
                    break
                yield chunk
    except:
        print "Error on read chunk"
        pass


