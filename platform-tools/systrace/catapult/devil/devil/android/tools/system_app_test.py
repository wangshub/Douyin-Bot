#!/usr/bin/env python
# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import os
import sys
import unittest

if __name__ == '__main__':
  sys.path.append(os.path.abspath(
      os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from devil import devil_env
from devil.android import device_utils
from devil.android.sdk import adb_wrapper
from devil.android.sdk import version_codes
from devil.android.tools import system_app

with devil_env.SysPath(devil_env.PYMOCK_PATH):
  import mock


class SystemAppTest(unittest.TestCase):

  def testDoubleEnableModification(self):
    """Ensures that system app modification logic isn't repeated.

    If EnableSystemAppModification uses are nested, inner calls should
    not need to perform any of the expensive modification logic.
    """
    # pylint: disable=no-self-use,protected-access
    mock_device = mock.Mock(spec=device_utils.DeviceUtils)
    mock_device.adb = mock.Mock(spec=adb_wrapper.AdbWrapper)
    type(mock_device).build_version_sdk = mock.PropertyMock(
        return_value=version_codes.LOLLIPOP)

    system_props = {}

    def dict_setprop(prop_name, value):
      system_props[prop_name] = value

    def dict_getprop(prop_name):
      return system_props.get(prop_name, '')

    mock_device.SetProp.side_effect = dict_setprop
    mock_device.GetProp.side_effect = dict_getprop

    with system_app.EnableSystemAppModification(mock_device):
      mock_device.EnableRoot.assert_called_once()
      mock_device.GetProp.assert_called_once_with(
          system_app._ENABLE_MODIFICATION_PROP)
      mock_device.SetProp.assert_called_once_with(
          system_app._ENABLE_MODIFICATION_PROP, '1')
      mock_device.reset_mock()

      with system_app.EnableSystemAppModification(mock_device):
        mock_device.EnableRoot.assert_not_called()
        mock_device.GetProp.assert_called_once_with(
            system_app._ENABLE_MODIFICATION_PROP)
        mock_device.SetProp.assert_not_called()
        mock_device.reset_mock()

    mock_device.SetProp.assert_called_once_with(
        system_app._ENABLE_MODIFICATION_PROP, '0')


if __name__ == '__main__':
  unittest.main()
