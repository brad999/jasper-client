# -*- coding: utf-8-*-
"""
A drop-in replacement for the Mic class that allows for all I/O to occur
over the terminal. Useful for debugging. Unlike with the typical Mic
implementation, Nikita is always active listening with local_mic.
"""
import logging

class Mic:
    prev = None

    def __init__(self, speaker, passive_stt_engine, active_stt_engine):
        self._logger = logging.getLogger(__name__)
        return

    def passiveListen(self, PERSONA):
        return True, "NIKITA"

    def activeListenToAllOptions(self, THRESHOLD=None, LISTEN=True,
                                 MUSIC=False):
        return [self.activeListen(THRESHOLD=THRESHOLD, LISTEN=LISTEN,
                                  MUSIC=MUSIC)]

    def activeListen(self, THRESHOLD=None, LISTEN=True, MUSIC=False):
        if not LISTEN:
            return self.prev

        input = raw_input("YOU: ")
        self.prev = input
        return input

    def say(self, speechType, phrase, OPTIONS=None):
        print("NIKITA: %s" % phrase)
        self._logger.transcript('Returned: %r|%r', speechType, phrase)
