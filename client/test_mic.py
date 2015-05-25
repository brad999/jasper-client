# -*- coding: utf-8-*-
"""
A drop-in replacement for the Mic class used during unit testing.
Designed to take pre-arranged inputs as an argument and store any
outputs for inspection. Requires a populated profile (profile.yml).
"""
import logging


class Mic:

    def __init__(self, inputs):
        self.inputs = inputs
        self.idx = 0
        self.outputs = []
        self._logger = logging.getLogger(__name__)

    def passiveListen(self, PERSONA):
        return True, "NIKITA"

    def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True,
                                 MUSIC=False):
        return [self.activeListen(THRESHOLD=THRESHOLD, LISTEN=LISTEN,
                                  MUSIC=MUSIC)]

    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        if not LISTEN:
            return self.inputs[self.idx - 1]

        input = self.inputs[self.idx]
        self.idx += 1
        return input

    def say(self, speechType, phrase, OPTIONS=None):
        self.outputs.append(phrase)
        self._logger.transcript('Returned: %r|%r', speechType, phrase)
