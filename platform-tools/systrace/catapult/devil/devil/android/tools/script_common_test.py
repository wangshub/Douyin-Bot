#!/usr/bin/env python
# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


import argparse
import sys
import tempfile
import unittest

from devil import devil_env
from devil.android import device_errors
from devil.android import device_utils
from devil.android.tools import script_common

with devil_env.SysPath(devil_env.PYMOCK_PATH):
  import mock  # pylint: disable=import-error

with devil_env.SysPath(devil_env.DEPENDENCY_MANAGER_PATH):
  from dependency_manager import exceptions


class GetDevicesTest(unittest.TestCase):

  def testNoSpecs(self):
    devices = [
        device_utils.DeviceUtils('123'),
        device_utils.DeviceUtils('456'),
    ]
    with mock.patch('devil.android.device_utils.DeviceUtils.HealthyDevices',
                    return_value=devices):
      self.assertEquals(
          devices,
          script_common.GetDevices(None, None))

  def testWithDevices(self):
    devices = [
        device_utils.DeviceUtils('123'),
        device_utils.DeviceUtils('456'),
    ]
    with mock.patch('devil.android.device_utils.DeviceUtils.HealthyDevices',
                    return_value=devices):
      self.assertEquals(
          [device_utils.DeviceUtils('456')],
          script_common.GetDevices(['456'], None))

  def testMissingDevice(self):
    with mock.patch('devil.android.device_utils.DeviceUtils.HealthyDevices',
                    return_value=[device_utils.DeviceUtils('123')]):
      with self.assertRaises(device_errors.DeviceUnreachableError):
        script_common.GetDevices(['456'], None)

  def testNoDevices(self):
    with mock.patch('devil.android.device_utils.DeviceUtils.HealthyDevices',
                    return_value=[]):
      with self.assertRaises(device_errors.NoDevicesError):
        script_common.GetDevices(None, None)


class InitializeEnvironmentTest(unittest.TestCase):

  def setUp(self):
    # pylint: disable=protected-access
    self.parser = argparse.ArgumentParser()
    script_common.AddEnvironmentArguments(self.parser)
    devil_env.config = devil_env._Environment()

  def testNoAdb(self):
    args = self.parser.parse_args([])
    script_common.InitializeEnvironment(args)
    with self.assertRaises(exceptions.NoPathFoundError):
      devil_env.config.LocalPath('adb')

  def testAdb(self):
    with tempfile.NamedTemporaryFile() as f:
      args = self.parser.parse_args(['--adb-path=%s' % f.name])
      script_common.InitializeEnvironment(args)
      self.assertEquals(
          f.name,
          devil_env.config.LocalPath('adb'))

  def testNonExistentAdb(self):
    with tempfile.NamedTemporaryFile() as f:
      args = self.parser.parse_args(['--adb-path=%s' % f.name])
    script_common.InitializeEnvironment(args)
    with self.assertRaises(exceptions.NoPathFoundError):
      devil_env.config.LocalPath('adb')


if __name__ == '__main__':
  sys.exit(unittest.main())

