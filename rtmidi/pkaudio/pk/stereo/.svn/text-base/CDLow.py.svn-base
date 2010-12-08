"""
	CDLow - Low level CDROM interface
	Written to replace CDAudio, CDDB and PyGAME.CD and 
		add functionality (skipping)
	Originally from the Gryphon CD player (http://gryphon.sourceforge.net/)
	
	Copyright 2001 (c) Christian Storgaard.
   	Changes made by Ron Kuslak <rds@rdsarts.com>, 2003-2004
	
	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from fcntl import ioctl
from CDROM import *
import os, struct

debug = 0

trayopen  = 0

NOSTATUS  = 0
PAUSED    = 1
STOPPED   = 2
NODISC    = 3
PLAYING   = 4
ERROR     = 5

tochdr_fmt   = "BB"
tocentry_fmt = "BBBix"
addr_fmt     = "BBB"+"x"*(struct.calcsize('i')-3)
region_fmt   = "BBBBBB"
subchnl_fmt  = "BBxBBiBBB"

class cd:
	path = "/dev/cdrom"
	start = end = None
	open = cd = 0
	last = (0,0,0)
	skip = 3	# In seconds
	data = 0	# Display Data-tracks

""" ####	Internal functions	####
    ####	    -- start --		####"""
def cd_open():
	if cd.cd > 0:
		cd.open = 1
		return 0
	else:
		try:
                        flags = os.O_RDONLY|os.O_NONBLOCK
			cd.cd = os.open(cd.path, flags)
			trayopen = 0
			return 0
		except:
			cd.status = NODISC
			trayopen = 1
			return 1
		
def cd_close():
	if cd.cd < 1:
		cd.open = 0
		return 0
	os.close(cd.cd)
	cd.cd   = 0
	cd.open = 0
	return 0

"""exit function"""
import atexit
atexit.register(cd_close)

""" ####	Internal functions	####
    ####	     -- end --		####"""

def stop():
#	cd_open()
	""" We don't care if there's a CD in or not, we're just stopping ;)"""
	if get_status() == PAUSED:
		try:
			ioctl(cd.cd, CDROMRESUME)
		except:
			pass
#	cd_open()
	try:
		ioctl(cd.cd, CDROMSTOP)
	except:
		pass
#	cd_close()

def pause():
	status = get_status()
#	cd_open()
	if status == PLAYING:
		ioctl(cd.cd, CDROMPAUSE)
	elif status == PAUSED:
		ioctl(cd.cd, CDROMRESUME)
#	cd_close()

def forward(val=None):
	if val!=None: skip(0,val,1)
	else: skip(0)

def rewind(val=None):
	if val!=None: skip(1,val,1)
	skip(1)

def goto(min, sec, frm=0):
	"""See if we have the last track to play in cache, else set to last on disc"""
	if cd.last == (0,0,0):
		if cd.end == None: get_header()
		cd.last = get_track_time(cd.end)
	try: play_msf(min, sec, frm, cd.last[0], cd.last[1], cd.last[2])
	except: pass

def skip(direction, amount=None, frames=0):
	if amount == None: amount = cd.skip
	if not frames: amount = amount*CD_FRAMES
	curmin, cursec, curfrm = get_current_timing()['abs']
	start = msf2frm(curmin,cursec,curfrm)
	"""Apply according to which direction we are skipping"""
	if direction == 1:start=start-amount
	else:start=start+amount
	startmin,startsec,startfrm=frm2msf(start)
	"""See if we have the last track to play in cache, else set to last on disc"""
	if cd.last == (0,0,0):
		if cd.end == None: get_header()
		cd.last = get_track_time(cd.end)
	try: play_msf(startmin, startsec, startfrm, cd.last[0], cd.last[1], cd.last[2])
	except: pass

def play(first,last=None):
	if last == None:last=first
	i=get_track_time(first)
	cd.last = get_track_time(last+1)
	play_msf(i[0],i[1],i[2],cd.last[0],cd.last[1],cd.last[2])

def play_msf(startmin, startsec, startfrm, endmin, endsec, endfrm):
#	cd_open()
	cd.last=(endmin,endsec,endfrm)
	region = struct.pack(region_fmt,startmin,startsec,startfrm,endmin,endsec,endfrm)
	ioctl(cd.cd, CDROMPLAYMSF, region)
#	cd_close()

def eject():
	cd_open()
	try:
		ioctl(cd.cd, CDROMSTOP)
		# Always unlock door before eject, in case something else locked it
		ioctl(cd.cd, CDROM_LOCKDOOR, 0)
	except:
		# ioctl(cd.cd, CDROMRESET)
		ioctl(cd.cd, CDROMSTOP)
		# Always unlock door before eject, in case something else locked it
		ioctl(cd.cd, CDROM_LOCKDOOR, 0)
	try:
		ioctl(cd.cd, CDROMEJECT_SW, 0)
		ioctl(cd.cd, CDROMEJECT)
	except:
		ioctl(cd.cd, CDROMEJECT_SW, 0)
		ioctl(cd.cd, CDROMEJECT)
#	cd_close()
	
def close():
#	cd_open()
	try:
		ioctl(cd.cd, CDROMCLOSETRAY)
	except:
		pass
#	cd_close()

def do_eject():
	if debug: print "Activated:\tCDLow.do_eject"
	cd_close()
	cd_open()
	global trayopen
	if debug: print "\tStatus:",trayopen
	ioctl(cd.cd, CDROMEJECT_SW, 0)
	if not trayopen:
		try:
			stop()
			if debug: print "\tStopped"
		except:
			pass
		eject()
		if debug: print "\tEjected Tray"
		cd.cd = 0
		cd.status = NODISC
		trayopen = 1
	else:
		close()
		if debug: print "\tClosed Tray"
		trayopen = 0
		cd_close()
		if debug: print "\tClosed CD"
		cd_open()
		if debug: print "\tOpened CD"
	return trayopen

def get_volume():
#	cd_open()
	try:
		return struct.unpack("BBBB",ioctl(cd.cd, CDROMVOLREAD, struct.pack("BBBB",0,0,0,0)))
		
	except:
		return (0,0,0,0)
#	cd_close()

def set_volume(frontleft,frontright=None,backleft=0,backright=0):
#	cd_open()
	if frontright == None: frontright = frontleft
	try:
		return struct.unpack("BBBB",ioctl(cd.cd, CDROMVOLCTRL, struct.pack("BBBB",frontleft,frontright,backleft,backright)))
		
	except:
		return 1
#	cd_close()

def get_status(time=0, all=0):
#	cd_open()
	result = 0
	i = 1
	while result == 0 and i < 5:
		try:	# If this fails then it's because it's happening too fast, just retry
			info = ioctl(cd.cd, CDROMSUBCHNL, struct.pack(subchnl_fmt, CDROM_MSF,0,0,0,0,0,0,0))
			drvstatus = get_drive_status()
			result = 1
		except:
			i = i +1
#	cd_close()
	format, status, track, something, absaddr, relmin, relsec, relfrm = struct.unpack(subchnl_fmt, info)
	absmin, abssec, absfrm = struct.unpack(addr_fmt, struct.pack("i", absaddr))
	zero = (1, 0,0,0, 0,0,0)
	if   status == CDROM_AUDIO_PLAY      : cd.status = PLAYING
	elif status == CDROM_AUDIO_PAUSED    : cd.status = PAUSED
	elif status == CDROM_AUDIO_COMPLETED :
		cd.status = STOPPED
		track,relmin,relsec,relfrm,absmin,abssec,absfrm = zero
	elif status == CDROM_AUDIO_ERROR     :
		cd.status = ERROR
		track,relmin,relsec,relfrm,absmin,abssec,absfrm = zero
	elif status == CDROM_AUDIO_INVALID   :
		cd.status = ERROR
		track,relmin,relsec,relfrm,absmin,abssec,absfrm = zero
	elif status == CDROM_AUDIO_NO_STATUS :
		cd.status = NOSTATUS
		track,relmin,relsec,relfrm,absmin,abssec,absfrm = zero
	if   drvstatus == CDS_NO_DISC :
		cd.status = NODISC
		track,relmin,relsec,relfrm,absmin,abssec,absfrm = zero
	if all: return {'status': drvstatus, 'format': format, 'status': status, 'track': track, 'something': something, 'absaddr': absaddr, 'relmin': relmin, 'relsec': relsec, 'relfrm': relfrm}
	elif time: return {'cur_t': track,'rel':(relmin,relsec,relfrm),'abs':(absmin,abssec,absfrm)}
	else: return cd.status

def get_disc_type():
#	cd_open()
	ret = ioctl(cd.cd, CDROM_DISC_STATUS)
#	cd_close()
	return ret

def get_drive_status():
#	cd_open()
	ret = 999
	ret = ioctl(cd.cd, CDROM_DRIVE_STATUS)
#	cd_close()
	return ret

def get_header():
#	cd_open()
	tochdr = struct.pack(tochdr_fmt, 0, 0)
	tochdr = ioctl(cd.cd, CDROMREADTOCHDR, tochdr)
	cd.start, cd.end = struct.unpack(tochdr_fmt, tochdr)
#	cd_close()

def get_track_time(trk):
	if cd.start == None:
		get_header()
	if   trk < 1: trk = 1
	elif trk > cd.end: trk = CDROM_LEADOUT
#	cd_open()
	toc = struct.pack(tocentry_fmt, trk, 0, CDROM_MSF, 0)
	toc = ioctl(cd.cd, CDROMREADTOCENTRY, toc)

	track, adrctrl, format, addr = struct.unpack(tocentry_fmt, toc)
	m, s, f = struct.unpack(addr_fmt, struct.pack("i", addr))

	adr = adrctrl & 0xf
	ctrl = (adrctrl & 0xf0) >> 4

	start = (m * CD_SECS + s) * CD_FRAMES + f	# 60 and 75
	data = 0
	if ctrl & CDROM_DATA_TRACK:
		data = 1
#	cd_close()
	return m,s,f,start,data

def get_track_length(first,last=None):
	if last==None: last=first+1
	off1min, off1sec, off1frm, off1, data1 = get_track_time(first)
	off2min, off2sec, off2frm, off2, data2 = get_track_time(last)
	
	lenmin,lensec,lenfrm=frm2msf(off2-off1)

	return off1min,off1sec,off1frm,lenmin,lensec,lenfrm,off1,data1

def get_tracks_id():
	get_header()
	offset = []
	data = []
	length = []
	tracklist = range(cd.start,cd.end+1)
	tracklist.append(CDROM_LEADOUT)
	for i in tracklist:
		m,s,f,lenm,lens,lenf,start,tdata = get_track_length(i)
		offset.append((m, s, f))
		data.append(tdata)
		if i <= cd.end:		# We don't want length of CDROM_LEADOUT ;)
			length.append((lenm, lens, lenf))#0)) 	# 0 is CDAudio's way
	tracks = {'start_t':cd.start, 'end_t':cd.end, 'offset': offset, 'length': length, 'id': disc_id(offset, cd.start, cd.end), 'data': data}
	tracks['cddb'] = get_cddb_id(tracks['id'][2:-1], tracks['id'][-1])
	return tracks

def get_current_timing():	# Wrapper for get_status(1)
	return get_status(1)

def disc_id(offset, first, last):
	track_frames = []
	checksum = long(0)
	for i in range(first-1, last):
		(min, sec, frame) = offset[i]
		checksum = checksum + id_sum(min*CD_SECS + sec)
		track_frames.append(min*CD_SECS*CD_FRAMES + sec*CD_FRAMES + frame)
	(min, sec, frame) = offset[last]
	track_frames.append(min*CD_SECS*CD_FRAMES + sec*CD_FRAMES + frame)

	total_time = (track_frames[-1] / CD_FRAMES) - (track_frames[0] / CD_FRAMES)

	discid = (int((checksum % 0xff) << 24) | total_time << 8 | last)

	return [discid,last]+track_frames[:-1]+[track_frames[-1]/CD_FRAMES]

def id_sum(s):
	sum = 0
	while s > 0:
		sum = sum + (s % 10)
		s = s / 10
	return sum

def frm2msf(frm):
	min = (frm / CD_FRAMES) / CD_SECS
	sec = (frm / CD_FRAMES) - (min * CD_SECS)
	frm = frm - ((min * CD_SECS) * CD_FRAMES + sec * CD_FRAMES)
	return min,sec,frm

def msf2frm(min,sec,frm):
	return min*CD_SECS*CD_FRAMES+sec*CD_FRAMES+frm

def get_cddb_id(tracks, disclen):
	checksum = long(0)
	for i in tracks:
		sum = 0
		mfs = (i / CD_FRAMES)
		while mfs > 0:
			sum = sum + (mfs % 10)
			mfs = mfs / 10
		checksum = checksum + sum
	tot_time = disclen - tracks[0] / CD_FRAMES
	return "%08x" % ((checksum % 0xff) << 24 | tot_time << 8 | len(tracks))


""" ####	Startup code	####
    ####			####"""

cd_open()
