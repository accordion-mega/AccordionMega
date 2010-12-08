"""
Scheduler plugin concept.
"""

import scheduler


class PluggedScheduler(scheduler.Scheduler):
    """ I don't really understand where I'm going with this plugin concept. """

    def __init__(self, sound, clock):
        scheduler.Scheduler.__init__(self, sound, clock)
        self.plugins = []

    def addPlugin(self, plugin):
        self.plugins.append(plugin)

    def render(self, target):
        for plugin in list(self.plugins):
            plugin.tick(self)
        scheduler.Scheduler.render(self, target)


class Plugin:
    """ Make the events all funky. """
    
    def tick(self, sched):
        pass

