# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import os

from devil import devil_env
from devil.android import device_blacklist
from devil.android import device_errors
from devil.android import device_utils


def AddEnvironmentArguments(parser):
  """Adds environment-specific arguments to the provided parser."""
  parser.add_argument(
      '--adb-path', type=os.path.realpath,
      help='Path to the adb binary')


def InitializeEnvironment(args):
  devil_dynamic_config = devil_env.EmptyConfig()
  if args.adb_path:
    devil_dynamic_config['dependencies'].update(
        devil_env.LocalConfigItem(
            'adb', devil_env.GetPlatform(), args.adb_path))

  devil_env.config.Initialize(configs=[devil_dynamic_config])


def AddDeviceArguments(parser):
  """Adds device and blacklist arguments to the provided parser."""
  parser.add_argument(
      '-d', '--device', dest='devices', action='append',
      help='Serial number of the Android device to use. (default: use all)')
  parser.add_argument('--blacklist-file', help='Device blacklist JSON file.')


def GetDevices(requested_devices, blacklist_file):
  """Gets a list of healthy devices matching the given parameters."""
  if not isinstance(blacklist_file, device_blacklist.Blacklist):
    blacklist_file = (device_blacklist.Blacklist(blacklist_file)
                      if blacklist_file
                      else None)

  devices = device_utils.DeviceUtils.HealthyDevices(blacklist_file)
  if not devices:
    raise device_errors.NoDevicesError()
  elif requested_devices:
    requested = set(requested_devices)
    available = set(str(d) for d in devices)
    missing = requested.difference(available)
    if missing:
      raise device_errors.DeviceUnreachableError(next(iter(missing)))
    return sorted(device_utils.DeviceUtils(d)
                  for d in available.intersection(requested))
  else:
    return devices

