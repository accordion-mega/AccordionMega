"""
Functions for dealing with povray.

    job_times = [] # keep track for averaging
    while indecies:
        job_time = time.time()

        ... [ job ] ...

        job_time = int(time.time() - job_time)
        job_times.append(job_time)
        avg_time = 0
        for jt in job_times:
            avg_time += jt
        avg_time = avg_time / len(job_times)
        min_rem = (avg_time*len(indecies)) / 60
        sec_rem = (avg_time*len(indecies)) % 60
        sec_rem = str(sec_rem).rjust(2)
        sec_rem = sec_rem.replace(' ', '0')
        time_string = ', %d:%s minutes remaining' % (min_rem, sec_rem)
        
"""

import os
import os.path
import sys
import popen2
import time

WIDTH = 266
HEIGHT = 200
NUM_CLOCK_DIGITS = 10


def extension(fpath):
    """ return the extension of fpath, not including the . """
    return fpath[fpath.rfind('.')+1:]


def isolder(fpath1, fpath2):
    """ Return True if fpath1 is older than fpath2 """
    return os.path.getmtime(fpath1) < os.path.getmtime(fpath2)
 

inline_msg = ''
def print_inline(msg):
    """ iteratively write and over-write a message on the same line. """
    global inline_msg
    # cover out tracks with spaces (weird)
    sys.stdout.write('\b' * len(inline_msg))
    sys.stdout.write(' ' * len(inline_msg))
    sys.stdout.write('\b' * len(inline_msg))
    sys.stdout.write(msg)
    sys.stdout.flush()
    if msg[-1:] == '\n':
        inline_msg = ''
    else:
        inline_msg = msg


spinner_data = '|/-\\|/-\\'
spinner_pos = 0
spinner_written = False
def tick_spinner(clear=False):
    """ Turn the spinner once. When the spinner should go away,
        pass True for clear. Some (most?) terminals will need something to get
        printed after the spinner is cleared, just to overwrite the hanging
        char. a newline should work.
    """
    global spinner_pos, spinner_data, spinner_written
    if clear:
        sys.stdout.write('\b')
        #sys.stdout.write(' ')
        sys.stdout.flush()
        spinner_pos = 0
    else:
        spinner_pos += 1
        if spinner_pos == len(spinner_data):
            spinner_pos = 0
        if spinner_written:
            sys.stdout.write('\b')
        sys.stdout.write(spinner_data[spinner_pos])
        sys.stdout.flush()
        spinner_written = True


def render_frame(name, clock=0, sr=0, er=0, sc=0, ec=0, basepath='',
                 preview=False, output=True, quality=11, pause=False,
                 png_path=None, pretend=False):
    """ render a frame for a given widget.
    basepath should become part of the name, this is run from cwd atm.
    """
    clock_str = str(clock)

    if png_path is None:
        png_path = os.path.join(basepath, name, name + clock_str + '.png')
    pov_path = os.path.join(basepath, name, name+'.pov')
    if not '.' in clock_str:
        clock_str = clock_str.zfill(NUM_CLOCK_DIGITS)
    if preview: preview = '+D0'
    else: preview = '-D0'
    if output: output = '+O'+png_path
    else: output = '-O'
    if pause: pause = '+P'
    else: pause = '-P'

    args = ('povray',
            pov_path,
            'Clock='+clock_str,
            output,
            '+L..',
            pause,
            preview,
            '+Q'+str(quality),
            '+R2',
            '+AM2',
            '+A0.3',
            '+W'+str(WIDTH),
            '+H'+str(HEIGHT),
            #'+SR'+str(sr), '+ER'+str(er), '+SC'+str(sc), '+EC'+str(ec),
            )
    
    if pretend:
        return

    try:
        global proc
        proc = popen2.Popen4(args)
        while proc.poll() is None:
            time.sleep(.1)
    except Exception, e:
        import signal
        os.kill(proc.pid, signal.SIGKILL)
        os.system('rm -f %s' % png_path)
        print '\n** POVRAY IMAGE NOT RENDERED'
        if e.__class__ == KeyboardInterrupt:
            sys.exit(0)
    return True


def get_old_images(path, frames):
    """ Returns a list of indecies of images that need updating.
    this needs to be integrated with a project (where is name located?)
    """
    name = os.path.basename(path)
    pov_path = os.path.join(path, name+'.pov')
    
    ret = []
    if not os.path.isfile(pov_path):
        return ret

    for i in range(frames+1):
        clock = str(i).zfill(NUM_CLOCK_DIGITS)
        fname = name + clock + '.png'
        img_path = os.path.join(path, fname)
        if not os.path.exists(img_path):
            ret.append(clock)
        elif isolder(img_path, pov_path):
            ret.append(clock)
    return ret



def get_modules(path=os.getcwd()):
    """ Return a list of valid module directories for a given path """
    ret = []
    for mname in os.listdir(path):
        fpath = os.path.join(path, mname)
        if os.path.isdir(fpath):
            pov_path = os.path.join(fpath, mname+'.pov')
            inc_path = os.path.join(path, mname+'.inc')
            has_pov = os.path.isfile(pov_path)
            has_inc = os.path.isfile(inc_path)
            if has_pov:
                ret.append(mname)
    return ret


def crop_pixmaps(path, mask, pretend=False):
    """ crop all pixmaps in a dir according to a masks.  This function
    does nothing in regards to validating modules. If the pixmaps
    exist and an entry exists in masks, the pixmaps get chopped.
    """
    from PyQt4.QtGui import QPixmap
    for fname in os.listdir(path):
        if extension(fname) == 'png':
            fpath = os.path.join(path, fname)
            pixmap = QPixmap(fpath)
            x, y, w, h = mask[0], mask[1], mask[2], mask[3]
            if pixmap.isNull() is False and \
               pixmap.width() > w and \
               pixmap.height() > h:
                pixmap = pixmap.copy(x, y, w, h)
                if pretend:
                    print 'PRETEND:',
                else:
                    pixmap.save(fpath, 'PNG')
                print 'wrote %s x=%i y=%i w=%i h=%i' % (fpath, x, y, w, h)
