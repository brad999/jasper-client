# -*- coding: utf-8-*-
"""
A drop-in replacement for the Mic class that allows for all I/O to occur
over the terminal. Useful for debugging. Unlike with the typical Mic
implementation, Nikita is always active listening with local_mic.
"""
import logging


class Mic:
    prev = None

    def __init__(self, speaker, passive_stt_engine,
                 active_stt_engine, db, profile):
        self._logger = logging.getLogger(__name__)
        self.db = db
        self.db_cursor = self.db.cursor()
        self.profile = profile
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
        if speechType == 'I':
            self.db_cursor.execute("INSERT INTO transcript (nikita_id, \
                                   create_timestamp, speech_type, \
                                   speech_text) VALUES (%s, now(), \
                                   %s, %s)", (self.profile['nikita_id'],
                                   speechType, phrase))
            self.db.commit()
