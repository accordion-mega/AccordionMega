#   Copyright (C) 2006 by Patrick Stinson                                 
#   patrickkidd@gmail.com                                                   
#                                                                         
#   This program is free software; you can redistribute it and/or modify  
#   it under the terms of the GNU General Public License as published by  
#   the Free Software Foundation; either version 2 of the License, or     
#   (at your option) any later version.                                   
#                                                                         
#   This program is distributed in the hope that it will be useful,       
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         
#   GNU General Public License for more details.                          
#                                                                         
#   You should have received a copy of the GNU General Public License     
#   along with this program; if not, write to the                         
#   Free Software Foundation, Inc.,                                       
#   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.  
#
"""
This is VERY high-level, and simply here for composition's sake.
"""

import os.path
import pk.widgets
import tempo
import selector
import spec


class ToolBox(pk.widgets.ToolBox):
    def __init__(self, parent=None):
        pk.widgets.ToolBox.__init__(self, parent)

        self.loopSelector = selector.Selector(self)
        self.loopScroller = pk.widgets.ScrollArea(self,
                                                   horizontal=False,
                                                   vertical=True,
                                                   color=spec.SCROLLPAD_COLOR)
        self.loopScroller.setWidget(self.loopSelector)
        self.loopScroller.v_pad.setFixedWidth(spec.SCROLLPAD_WIDTH)

        self.effectSelector = selector.Selector(self)
        self.effectScroller = pk.widgets.ScrollArea(self,
                                                    horizontal=False,
                                                    vertical=True,
                                                   color=spec.SCROLLPAD_COLOR)
        self.effectScroller.v_pad.setFixedWidth(spec.SCROLLPAD_WIDTH)
        self.effectScroller.setWidget(self.effectSelector)

        self.tempoAdjuster = tempo.Adjuster(self)
        
        self.addItem(self.loopScroller, 'loops')
        self.addItem(self.effectScroller, 'effects')
        self.addItem(self.tempoAdjuster, 'tempo')


def frames_per_beat(tempo, samplerate, channels=2):
    bps = float(tempo) / 60 / channels
    return int(samplerate / bps) / 2


import wave
def guess_beats(fpath, filetempo=140):
    try:
        wavfile = wave.open(fpath, 'r')
    except wave.Error, e:
        print '*** ERROR opening %s' % fpath
        raise e
    frames = wavfile.getnframes()
    channels = wavfile.getnchannels()
    samplerate = wavfile.getframerate() * channels
    fpb = frames_per_beat(140, samplerate, channels)
    beats = frames / fpb
    rem = frames % float(fpb)
    if rem > (fpb * .5):
        beats += 1
    return beats


def string_cmp(a, b):
    """ compare strings based on int values. """
    try:
        a = int(a.split()[0])
    except:
        pass
    try:
        b = int(b.split()[0])
    except:
        pass
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


def file_2_dict(fpath):
    ret = {}
    if os.path.isfile(fpath):
        for line in open(fpath).readlines():
            if line.strip().startswith('#'):
                continue
            key, value = line.split(' = ')
            key = key.strip()
            value = value.strip()
            ret[key] = value
    return ret


SONGPART_COLORS = {'bass' : 'red',
                   'drums' : 'purple',
                   'lead' : 'blue',
                   'pads' : 'yellow',
                   'misc' : 'orange',
                   }


def load_all(toolbox):
    from PyQt4.QtGui import QColor
    import parts, spec, synths
    import engine
    loops = toolbox.loopSelector
    effects = toolbox.effectSelector

    fpaths = []
    for song in os.listdir(spec.LOOPS):
        songpath = os.path.join(spec.LOOPS, song)
        manifest = file_2_dict(os.path.join(songpath, 'manifest.txt'))
        for part in os.listdir(songpath):
            partpath = os.path.join(songpath, part)
            if os.path.isdir(partpath):
                for fname in os.listdir(partpath):
                    if fname.endswith('.wav'):
                        fpath = os.path.join(partpath, fname)
                        beats = guess_beats(fpath)
                        tempo = None
                        if 'tempo' in manifest:
                            tempo = float(manifest['tempo'])
                        fpaths.append((fpath, beats, part, tempo))
    fpaths.sort(string_cmp)
    for fpath, beats, songpart, tempo in fpaths:
        fname = os.path.basename(fpath)
        sample = synths.Sample()
        sample.filetempo = tempo
        sample.filepath = fpath

        part = parts.LoopPart(sample)
        part.text = fname[:fname.find('.')]
        part.songpart = songpart
        color = QColor(SONGPART_COLORS.get(songpart, 'grey'))
        part.base_color(color)
        if beats > 0:
            part.text += '\n(%i beats)' % beats
            part.pattern = engine.Pattern(beats=beats)
            part.pattern.add(engine.Note(0, 64 * beats, 69))
            part.pattern.synth = sample
        loops.add(part)
    for name in ('JASDelayNoInterpolation', 'JASResonantLowPassFilter'):
        effect = synths.Synth()
        effect.name = name
        effects.add(parts.EffectPart(effect))

#    patterns = os.listdir(spec.PATTERNS)
#    patterns.sort(string_cmp)
#    for fname in patterns:
#        if fname.lower().endswith('.xml'):
#            fpath = os.path.join(spec.PATTERNS, fname)
#            part = parts.PatternPart(scsynth.read_pattern(fpath))
#            patterns_.add(part)


if __name__ == '__main__':
    from PyQt4.QtGui import QColor
    import parts
    from pk.widgets.utils import run_widget
    class TestToolBox(ToolBox):
        def __init__(self):
            ToolBox.__init__(self)
            self.setAutoFillBackground(True)
            self.palette().setColor(self.backgroundRole(),
                                    QColor(136, 136, 136))
            load_all(self)
            self.resize(spec.PART_WIDTH + 60, 600)
    run_widget(TestToolBox)
