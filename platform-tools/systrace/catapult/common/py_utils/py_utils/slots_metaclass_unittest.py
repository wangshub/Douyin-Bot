# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from py_utils import slots_metaclass

class SlotsMetaclassUnittest(unittest.TestCase):

  def testSlotsMetaclass(self):
    class NiceClass(object):
      __metaclass__ = slots_metaclass.SlotsMetaclass
      __slots__ = '_nice',

      def __init__(self, nice):
        self._nice = nice

    NiceClass(42)

    with self.assertRaises(AssertionError):
      class NaughtyClass(NiceClass):
        def __init__(self, naughty):
          super(NaughtyClass, self).__init__(42)
          self._naughty = naughty

      # Metaclasses are called when the class is defined, so no need to
      # instantiate it.

    with self.assertRaises(AttributeError):
      class NaughtyClass2(NiceClass):
        __slots__ = ()

        def __init__(self, naughty):
          super(NaughtyClass2, self).__init__(42)
          self._naughty = naughty  # pylint: disable=assigning-non-slot

      # SlotsMetaclass is happy that __slots__ is defined, but python won't be
      # happy about assigning _naughty when the class is instantiated because it
      # isn't listed in __slots__, even if you disable the pylint error.
      NaughtyClass2(666)
