"""

class Ripper:
    get_tracks()
        FOUND_DISC_INFO
        FOUND_TRACK_INFO
        CDDB_DONE
    rip_n_encode()
        ...
    event()
        abstract
    check_cd()
        DISC_CHANGED

    is_ripping
    is_encoding
    cd_status
    is_cddbing


class Event:
    type

    ...

    FOUND_DISC_INFO
        query_info
    FOUND_TRACK_INFO
        tracknum
        read_info
    CDDB_DONE
        artist
        count
        album
        genre
        year
        tracklist
    STATUS_UPDATE
        tracknum
        state        'rip', 'enc', 'rip_error', 'enc_error'
        percent      100 == done
    DISC_CLEARED
    NEW_DISC
        state
"""

import fcntl
import os, sys, signal, re, string, socket, time, popen2, threading, Queue
from random import Random
from threading import *
import PyCDDB, cd_logic, CDROM, genres, CDLow

try:
    import xattr
    HAVE_XATTR = True
except:
    HAVE_XATTR = False


#assume that everyone puts their music in ~/MyMusic
#LIBRARY = os.path.expanduser('~')+'/MyMusic'
LIBRARY='/var/lib/mpd/music/'

#RIPPER options
RIPPER = 'cdda2wav'
RIPPER_DEV = '/dev/cdrom'
RIPPER_LUN = 'ATAPI:0,1,0'
RIPPER_OPTS = '-x -H'

EJECT_AFTER_RIP = False

#ENCODER options
ENCODER = 'OGG'

MP3_ENCODER = 'lame'
MP3_ENCODER_OPTS = '--vbr-new -b160 --nohist --add-id3v2'

OGG_ENCODER = 'oggenc'
OGG_ENCODER_OPTS = '-q5'

#CDDB Server and Options
CDDB_SERVER = 'http://freedb.freedb.org/~cddb/cddb.cgi'



# EVENTS
FOUND_DISC_INFO = 1
FOUND_TRACK_INFO = 2
CDDB_DONE = 3
STATUS_UPDATE = 4
DISC_CLEARED = 5

class Event:
    def __init__(self, type):
        self.type = type


# My gentoo python doesn't have universal line ending support compiled in
# and these guys (cdda2wav and lame) use CR line endings to pretty-up their output.
## def myreadline(file):
##     '''Return a line of input using \r or \n as terminators'''
##     line = ''
##     while '\n' not in line and '\r' not in line:
##         char = ''
##         try:
##             char = file.read(1)
##         except IOError:
##             pass
##         if char:
##             line += char
##         else:
##             time.sleep(.1)
##     return line
def myreadline(file):
    '''Return a line of input using \r or \n as terminators'''
    line = ''
    while '\n' not in line and '\r' not in line:
        char = file.read(1)
        if char == '': return line
        line += char
    return line
    

def which(filename):
    '''Return the full path of an executable if found on the path'''
    if (filename == None) or (filename == ''):
        return None

    env_path = os.getenv('PATH').split(':')
    for p in env_path:
        if os.access(p+'/'+filename, os.X_OK):
            return p+'/'+filename
    return None


def strip_illegal(instr):
    '''remove illegal (filename) characters from string'''
    str = instr
    str = str.strip()
    str = string.translate(str, string.maketrans(r'/+{}*.?', r'--()___'))
    return str


class Ripper:
    '''Rip and Encode a CD'''
    def __init__(self, dev=RIPPER_DEV):

        # Defaults and Misc
        self.cddb_thd = None
        self.ripper_thd = None
        self.encoder_thd = None
        self.is_ripping = False
        self.is_encoding = False
        self.is_cddbing = False
        self.stop_request = False
        self.dev = dev

        cd_logic.set_dev(dev)
        status = cd_logic.check_dev()
        if status == -1:
            self.drive_exists = False
        else:
            self.drive_exists = True
        self.disc_id = None


    def runit(self, it):
        '''Run a function in a thread'''
        thd_it = Thread(name='mythread', target=it)
        thd_it.setDaemon(True)
        thd_it.start()
        return thd_it


    def stop(self, it):
        '''Stop current rip/encode process'''
        self.stop_request = True


    def get_tracks(self):
        '''Get the track info (cddb and cd)'''
        self.is_cddbing = True
        stuff = self.get_cddb()
        (count, artist, album, genre, year, tracklist) = stuff
        #print count, artist, album, genre, year, tracklist
        
        self.artist = artist
        self.count = count
        self.album = album
        self.genre = genre
        self.year = year
        self.tracklist = tracklist

        event = Event(CDDB_DONE)
        event.artist = artist
        event.album = album
        event.count = count
        event.genre = genre
        event.year = year
        event.tracklist = tracklist
        self.ripper_event(event)

        self.is_cddbing = False


    def get_cddb(self):
        '''Query cddb for track and cd info'''
        count = artist = genre = album = year = ''
        tracklist = []
        tracktime = []

        #Note: all the nested try statements are to ensure that as much
        #info is processed as possible.  One exception should not stop
        #the whole thing and return nothing.

        try:
            count = cd_logic.total_tracks()
            cddb_id = cd_logic.get_cddb_id()

            #PyCDDB wants a string delimited by spaces, go figure.
            cddb_id_string = ''
            for n in cddb_id:
                cddb_id_string += str(n)+' '
            #print disc_id
            #print cddb_id, cddb_id_string

            for i in range(count):
                tracktime = cd_logic.get_track_time_total(i+1)
                track_time = time.strftime('%M:%S', time.gmtime(tracktime))
                tracklist.append( ('Track%i' % i, track_time) )

            try:
                db = PyCDDB.PyCDDB(CDDB_SERVER)
                query_info = db.query(cddb_id_string)
                #print query_info
                
                event = Event(FOUND_DISC_INFO)
                event.query_info = query_info
                self.ripper_event(event)

                #make sure we didn't get an error, then query CDDB
                if len(query_info) > 0:
                    rndm = Random()
                    index = rndm.randrange(0, len(query_info))
                    read_info = db.read(query_info[index])
                    #print read_info

                    event = Event(FOUND_TRACK_INFO)
                    event.tracknum = index
                    event.read_info = read_info
                    self.ripper_event(event)

                    try:
                        (artist, album) = query_info[index]['title'].split('/')
                        artist = artist.strip()
                        album = album.strip()
                        genre = query_info[index]['category']
                        if genre in ['misc', 'data']:
                            genre = 'Misc'

                        print query_info['year']
                        print read_info['EXTD']
                        print read_info['YEARD']

                        #x = re.match(r'.*YEAR: (.+).*',read_info['EXTD'])
                        #if x:
                        #   print x.group(1)
                        #   year = x.group(1)
                    except:
                        pass

                    if len(read_info['TTITLE']) > 0:
                        for i in range(count):
                            try:
                                track_name = read_info['TTITLE'][i]
                                track_time = tracklist[i][1]
                                #print i, track_name, track_time
                                tracklist[i] = (track_name, track_time)
                            except:
                                pass
            except Exception, e:
                print e
                pass

        except Exception, e:
            print e
            pass
        return count, artist, album, genre, year, tracklist


    def get_cdda2wav(self, tracknum, track):
        '''Run cdda2wav to rip a track from the CD'''
        cdda2wav_cmd = RIPPER
        cdda2wav_dev = RIPPER_DEV
        cdda2wav_lun = RIPPER_LUN
        cdda2wav_args = '-A %s -D %s -t %d "%s"' % (
            cdda2wav_lun, cdda2wav_dev, tracknum+1, strip_illegal(track))
        cdda2wav_opts =  RIPPER_OPTS
        #print cdda2wav_opts, cdda2wav_args

        cmd = cdda2wav_cmd+' '+cdda2wav_opts+' '+cdda2wav_args

        print cmd
        
        thing = popen2.Popen4(cmd)
        outfile = thing.fromchild
        #fcntl.fcntl(outfile.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

        #status = thing.poll()
        #while status == -1:
        while True:
            line = myreadline(outfile)
            if line:
                #print line
                x = re.search('(\d{1,3})%', line)
                if x:
                    percent = int(x.group(1))
                    self._status_update(tracknum, 'rip', percent,
                                        strip_illegal(track))
            else:
                break
            #status = thing.poll()
            if self.stop_request:
                break
        #print 'cdda2wav finished with status (%i)' % status

        if self.stop_request:
            os.kill(thing.pid, signal.SIGKILL)

        code = thing.wait()
        self._status_update(tracknum, 'rip', 100, strip_illegal(track))
        #print code
        return code


    def get_lame(self, tracknum, track, artist, genre, album, year):
        '''Run lame to encode a wav file to mp3'''
        try:
            int_year = int(year)
        except:
            int_year = 1

        lame_cmd = MP3_ENCODER
        lame_opts = MP3_ENCODER_OPTS
        lame_tags = '--ta "%s" --tt "%s" --tl "%s" --tg "%s" --tn %d --ty %d' % (
                                artist, track, album, genre, tracknum+1, int_year)
        lame_args = '"%s" "%s"' % (strip_illegal(track)+'.wav', strip_illegal(track)+'.mp3')

        #print lame_opts, lame_tags, lame_args

        thing = popen2.Popen4(lame_cmd+' '+lame_opts+' '+lame_tags+' '+lame_args )
        outfile = thing.fromchild

        while True:
            line = myreadline(outfile)
            if line:
                #print line
                #for some reason getting this right for lame was a royal pain.
                x = re.match(r"^[\s]+([0-9]+)/([0-9]+)", line)
                if x:
                    percent = int(100 * (float(x.group(1)) / float(x.group(2))))
                    self._status_update(tracknum, 'enc', percent,
                                        strip_illegal(track))
            else:
                break
            if self.stop_request:
                break

        if self.stop_request:
            os.kill(thing.pid, signal.SIGKILL)
        elif HAVE_XATTR:
            try:
                filename = strip_illegal(track)+'.mp3'
                xattr.setxattr(filename, 'user.Title', track)
                xattr.setxattr(filename, 'user.Artist', artist)
                xattr.setxattr(filename, 'user.Album', album)
                xattr.setxattr(filename, 'user.Genre', genre)
                xattr.setxattr(filename, 'user.Track', '%d' % tracknum)
                xattr.setxattr(filename, 'user.Year', year)
            except:
                pass

        code = thing.wait()
        self._status_update(tracknum, 'enc', 100, strip_illegal(track))
        #print code
        return code


    def get_ogg(self, tracknum, track, artist, genre, album, year):
        '''Run oggenc to encode a wav file to ogg'''
        try:
            int_year = int(year)
        except:
            int_year = 1

        ogg_cmd = OGG_ENCODER
        ogg_opts = OGG_ENCODER_OPTS
        ogg_tags = '-a "%s" -t "%s" -l "%s" -G "%s" -N %d -d %d' % (
            artist, track, album, genre, tracknum+1, int_year)
        ogg_args = '"%s"' % (strip_illegal(track)+'.wav')

        #print ogg_opts, ogg_tags, ogg_args

        thing = popen2.Popen4(ogg_cmd+' '+ogg_opts+' '+ogg_tags+' '+ogg_args )
        outfile = thing.fromchild
        #fcntl.fcntl(outfile.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

        #status = thing.poll()
        #while status == -1:
        while True:
            line = myreadline(outfile)
            if line:
                #print line
                #for some reason getting this right for ogg was a royal pain.
                x = re.match('^.*\[[\s]*([.0-9]+)%\]', line)
                if x:
                    percent = float(x.group(1))
                    self._status_update(tracknum, 'enc', percent,
                                        strip_illegal(track))
            else:
                break
            #status = thing.poll()
            if self.stop_request:
                break
        #print 'oggenc finished with status (%i)' % status

        if self.stop_request:
            os.kill(thing.pid, signal.SIGKILL)
        elif HAVE_XATTR:
            try:
                filename = strip_illegal(track)+'.ogg'
                xattr.setxattr(filename, 'user.Title', track)
                xattr.setxattr(filename, 'user.Artist', artist)
                xattr.setxattr(filename, 'user.Album', album)
                xattr.setxattr(filename, 'user.Genre', genre)
                xattr.setxattr(filename, 'user.Track', '%d' % tracknum)
                xattr.setxattr(filename, 'user.Year', year)
            except:
                    pass

        code = thing.wait()
        self._status_update(tracknum, 'enc', 100, strip_illegal(track))
        #print code
        return code


    def rip_n_encode(self, genre=None):
        '''Process all selected tracks (rip and encode)'''
        if genre:
            self.genre = genre
        try: os.mkdir(LIBRARY)
        except: pass
        try: os.chdir(LIBRARY)
        except: pass

        if self.count and self.artist and self.album and self.genre:
            disc = '%s - %s' % (self.artist, self.album)
            path = os.path.join(LIBRARY, self.genre, disc)

            try: os.makedirs(path)
            except: pass            
            try: os.chdir(path)
            except: pass
            
        self.stop_request = False

        #the queue to feed tracks from ripper to encoder
        self.wavqueue = Queue.Queue(1000)

        self.ripper_thd = self.runit(self.ripit)
        self.encoder_thd = self.runit(self.encodeit)


    def ripit(self):
        '''Thread to rip all selected tracks'''
        self.is_ripping = True
        self.tmp_queue = []
        for i in range(self.count):
            if self.stop_request:
                break

            # if RIP_THIS_TRACK:
            track = self.tracklist[i][0]
            track = str(i).zfill(2)+'_' + track
            #print i, track
            status = self.get_cdda2wav(i, track)
            if status <> 0:
                print 'cdda2wav died %d' % status
                self._status_update(i, 'rip_error', 0)
            else:
                #push this track on the queue for the encoder
                self.tmp_queue.append((track, i))
            # fi RIP_THIS_TRACK

        #push None object to tell encoder we're done
        for entry in self.tmp_queue:
            self.wavqueue.put(entry)
        self.wavqueue.put((None, None))

        self.is_ripping = False
        cd_logic.stop()
        if EJECT_AFTER_RIP:
            cd_logic.eject()


    def encodeit(self):
        '''Thread to encode all tracks from the wavqueue'''
        self.is_encoding = True
        while True:
            if self.stop_request:
                break
            (track, tracknum) = self.wavqueue.get(True)
            if track == None:
                break

            if ENCODER == 'MP3':
                status = self.get_lame(tracknum, track, self.artist, self.genre, self.album, self.year)
            else:
                status = self.get_ogg(tracknum, track, self.artist, self.genre, self.album, self.year)
                
            if status <> 0:
                print 'encoder died %d' % status
                self._status_update(tracknum, 'enc_error', 0)
            try: os.unlink(strip_illegal(track)+".wav")
            except:	pass
            try: os.unlink(strip_illegal(track)+".inf")
            except:	pass

        self.is_encoding = False
        del self.wavqueue


    def _status_update(self, tracknum, state, percent, track=None):
        '''Callback from rip/encode threads to update display
        state in ('rip', 'env', 'rip_error', 'enc-error')
        '''
        event = Event(STATUS_UPDATE)
        event.tracknum = tracknum
        event.state = state
        event.percent = percent
        event.track = track
        event.genre = self.genre
        event.album = self.album
        event.artist = self.artist
        self.ripper_event(event)


    def read_disc_info(self):
        """ emit an event if cd status has changed. """
        if self.is_ripping:
            return
        elif CDLow.get_drive_status() in [CDROM.CDS_TRAY_OPEN, CDROM.CDS_NO_DISC, -1]:
            self.disc_id = None
            return
        elif CDLow.get_disc_type() != CDROM.CDS_AUDIO:
            return


        disc_id = cd_logic.get_disc_id()
        #if self.disc_id <> disc_id:
        self.disc_id = disc_id
        self.cddb_thd = self.runit(self.get_tracks)


    def ripper_event(self, e):
        """ Thread event. """
        pass




if __name__ == '__main__':
    LIBRARY = os.path.join(os.getcwd(), 'tests')
    class TestRipper(Ripper):
        def ripper_event(self, e):
            if e.type == STATUS_UPDATE:
                print e.__dict__
    ripper = TestRipper()
    ripper.get_tracks()
    ripper.rip_n_encode()
    while ripper.is_ripping or ripper.is_encoding:
        time.sleep(1)
    print 'done'
