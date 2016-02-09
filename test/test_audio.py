#!/usr/bin/env python

from __future__ import absolute_import

from ._helper import AuraTestCase

class TestTrack_ReturnedAudioMimetype(AuraTestCase):

    def setUp(self):
        super(TestTrack_ReturnedAudioMimetype,self).setUp()


    def test_mime_mpeg(self):
        for item in self.items_all_formats():
            rv = self.request_audio(item.id, headers=[('Accept','audio/mpeg')])
            self.assertEquals(rv.mimetype, 'audio/mpeg')

    def test_mime_wav(self):
        for item in self.items_all_formats():
            rv = self.request_audio(item.id, headers=[('Accept','audio/x-wav')])
            self.assertEquals(rv.mimetype, 'audio/x-wav')

    def test_mime_ogg(self):
        for item in self.items_all_formats():
            rv = self.request_audio(item.id, headers=[('Accept','audio/ogg')])
            self.assertEquals(rv.mimetype, 'audio/ogg')

    def test_mime_flac(self):
        for item in self.items_all_formats():
            rv = self.request_audio(item.id, headers=[('Accept','audio/x-flac')])
            self.assertIn(rv.mimetype, ['audio/flac', 'audio/x-flac'])

    def test_mime_glob(self):
        for item in self.items_all_formats():
            rv = self.request_audio(item.id, headers=[('Accept','audio/*')])
            self.assertEqual(rv.mimetype, self.item_mime(item))

class TestTrack_Audio(AuraTestCase):

    def setUp(self):
        super(TestTrack_Audio,self).setUp()

    def _test_audio(self,format):
        items = self.item_query(u"format:{}".format(format))
        for item in items:
            self.assertEqual(item['format'],format)
            rv = self.request_audio(item.id)
            self.assertEqual(len(rv.data),self.item_filesize(item))

    def test_audio_ogg(self):
        self._test_audio("OGG")

    def test_audio_flac(self):
        self._test_audio("FLAC")

    def test_audio_mpeg(self):
        self._test_audio("MP3")
