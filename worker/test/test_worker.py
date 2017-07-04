#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from .. import Worker


class WorkerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.worker = Worker()
