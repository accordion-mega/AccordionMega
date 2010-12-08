"""
	cd_logic.py
		Uses the CD library to control the CD and return it's status.

	Copyright 2003 Ron Kuslak <rds@rdsarts.com>
		All rights reserved.

	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License.

	This program is distributed in the hope that it will be useful
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
import CDLow as cd

updated = False

def set_dev(dev='/dev/cdrom'):
	""" Changes the CD device. Makes change. Dances poorly. """
	cd.cd_close()
	cd.cd.path = str(dev)
	cd.cd_open()
	updated = False
	return

def get_disc_id():
	temp = cd.get_tracks_id()
	id = temp['id']
	return int(id[0])

def get_cddb_id():
	temp = cd.get_tracks_id()
	id = temp['id']
	return id

def get_track_time():
	min, sec, temp = cd.get_status(1)['rel']
	return ((min * 60) + sec)

def get_track_time_total(track=None):
	if not track: track = current_track()
	t1, t2, t3, min, sec, t4, t5, t6 = cd.get_track_length(track)
	return ((min * 60) + sec)

def get_dev():
	return str(cd.cd.path)

def check_dev():
	# print cd.get_drive_status()
	try:
		return cd.get_drive_status()
	except IOError, err:
		print "IOError. Passing 0. Error was " + str(err)
		return -1

def total_tracks():
	#try:
	return cd.get_tracks_id()['end_t']
	# return int(cd_info['end_t'])
	#except :
	#	return 0
	#excect: # We should not reach here!
	#	print 'ERROR IN cd.py - total_tracks(). Please report this error.'
	#	return

def current_track():
	# try:
		temp = cd.get_status(1)
		return int(temp['cur_t'])
	# except:
		return -1
def update():
	try:
		status = cd.get_status()
	except:
		status = 0

	if status == 0:
		updated = True

def get_status():
	""" Returns CD's playing state. Yes, this is just a wrapper around
	    get_status. DEAL. ;)"""
	try:
		status = cd.get_status()
	except:
		# print "Error in play_pause"
		# # TODO: Do something. :P
		return 0
	return status

def play(track = 1):
	cd.play(track, total_tracks())

def stop():
	cd.stop()
	update()

def eject():
	cd.eject()
	update()

def next():
	"""	Advances CD one track, or puts it at track 1 if at last.	"""

	next = current_track() + 1
	last_t = total_tracks()
	if next < last_t:
		play(next)
	else:
		play(1)
	update()
	return 0

def prev():
	prev = current_track() - 1

	if prev == 0:
		prev = (total_tracks() - 1)

	play(prev)
	update()
	return 0

def pause():
	cd.pause()
	update()

def jump(seconds):
	cd.skip(0, seconds)
