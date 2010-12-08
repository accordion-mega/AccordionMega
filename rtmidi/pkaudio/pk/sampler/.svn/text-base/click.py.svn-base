class ClickTrack:

    def __init__(self, server, sequencer):
        self.click_stream = None
        self.click_pattern = sequencer.Pattern([sequencer.Note(0, 16, 60)])
        self.click_pattern.beats = 1
        self.click_synth = sequencer.Sample()

    def toggle(self, on):
        if on and self.click_stream is None:
            self.click_stream = self.register(self.click_synth,
                                              self.click_pattern)
        elif self.click_stream:
            self.deregister(self.click_stream)
            self.click_stream = None

    def set_file(self, fpath):
        wason = bool(self.click_stream)
        self.toggle(False)
        self.click_synth['bufnum'] = self.loader.load(fpath)
        self.toggle(wason)
