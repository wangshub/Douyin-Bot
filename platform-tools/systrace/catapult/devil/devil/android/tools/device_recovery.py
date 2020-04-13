#!/usr/bin/env python
# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""A script to recover devices in a known bad state."""

import argparse
import logging
import os
import psutil
import signal
import sys

if __name__ == '__main__':
  sys.path.append(
      os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   '..', '..', '..')))
from devil.android import device_blacklist
from devil.android import device_errors
from devil.android import device_utils
from devil.android.sdk import adb_wrapper
from devil.android.tools import device_status
from devil.android.tools import script_common
from devil.utils import logging_common
from devil.utils import lsusb
# TODO(jbudorick): Resolve this after experimenting w/ disabling the USB reset.
from devil.utils import reset_usb  # pylint: disable=unused-import

logger = logging.getLogger(__name__)


def KillAllAdb():
  def get_all_adb():
    for p in psutil.process_iter():
      try:
        # Note: p.as_dict is compatible with both older (v1 and under) as well
        # as newer (v2 and over) versions of psutil.
        # See: http://grodola.blogspot.com/2014/01/psutil-20-porting.html
        pinfo = p.as_dict(attrs=['pid', 'name', 'cmdline'])
        if 'adb' == pinfo['name']:
          pinfo['cmdline'] = ' '.join(pinfo['cmdline'])
          yield p, pinfo
      except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

  for sig in [signal.SIGTERM, signal.SIGQUIT, signal.SIGKILL]:
    for p, pinfo in get_all_adb():
      try:
        pinfo['signal'] = sig
        logger.info('kill %(signal)s %(pid)s (%(name)s [%(cmdline)s])', pinfo)
        p.send_signal(sig)
      except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
  for _, pinfo in get_all_adb():
    try:
      logger.error('Unable to kill %(pid)s (%(name)s [%(cmdline)s])', pinfo)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
      pass


def RecoverDevice(device, blacklist, should_reboot=lambda device: True):
  if device_status.IsBlacklisted(device.adb.GetDeviceSerial(),
                                 blacklist):
    logger.debug('%s is blacklisted, skipping recovery.', str(device))
    return

  if should_reboot(device):
    try:
      device.WaitUntilFullyBooted(retries=0)
    except (device_errors.CommandTimeoutError,
            device_errors.CommandFailedError,
            device_errors.DeviceUnreachableError):
      logger.exception('Failure while waiting for %s. '
                       'Attempting to recover.', str(device))
    try:
      try:
        device.Reboot(block=False, timeout=5, retries=0)
      except device_errors.CommandTimeoutError:
        logger.warning('Timed out while attempting to reboot %s normally.'
                       'Attempting alternative reboot.', str(device))
        # The device drops offline before we can grab the exit code, so
        # we don't check for status.
        try:
          device.adb.Root()
        finally:
          # We are already in a failure mode, attempt to reboot regardless of
          # what device.adb.Root() returns. If the sysrq reboot fails an
          # exception willbe thrown at that level.
          device.adb.Shell('echo b > /proc/sysrq-trigger', expect_status=None,
                           timeout=5, retries=0)
    except (device_errors.CommandFailedError,
            device_errors.DeviceUnreachableError):
      logger.exception('Failed to reboot %s.', str(device))
      if blacklist:
        blacklist.Extend([device.adb.GetDeviceSerial()],
                         reason='reboot_failure')
    except device_errors.CommandTimeoutError:
      logger.exception('Timed out while rebooting %s.', str(device))
      if blacklist:
        blacklist.Extend([device.adb.GetDeviceSerial()],
                         reason='reboot_timeout')

    try:
      device.WaitUntilFullyBooted(
          retries=0, timeout=device.REBOOT_DEFAULT_TIMEOUT)
    except (device_errors.CommandFailedError,
            device_errors.DeviceUnreachableError):
      logger.exception('Failure while waiting for %s.', str(device))
      if blacklist:
        blacklist.Extend([device.adb.GetDeviceSerial()],
                         reason='reboot_failure')
    except device_errors.CommandTimeoutError:
      logger.exception('Timed out while waiting for %s.', str(device))
      if blacklist:
        blacklist.Extend([device.adb.GetDeviceSerial()],
                         reason='reboot_timeout')


def RecoverDevices(devices, blacklist, enable_usb_reset=False):
  """Attempts to recover any inoperable devices in the provided list.

  Args:
    devices: The list of devices to attempt to recover.
    blacklist: The current device blacklist, which will be used then
      reset.
  """

  statuses = device_status.DeviceStatus(devices, blacklist)

  should_restart_usb = set(
      status['serial'] for status in statuses
      if (not status['usb_status']
          or status['adb_status'] in ('offline', 'missing')))
  should_restart_adb = should_restart_usb.union(set(
      status['serial'] for status in statuses
      if status['adb_status'] == 'unauthorized'))
  should_reboot_device = should_restart_adb.union(set(
      status['serial'] for status in statuses
      if status['blacklisted']))

  logger.debug('Should restart USB for:')
  for d in should_restart_usb:
    logger.debug('  %s', d)
  logger.debug('Should restart ADB for:')
  for d in should_restart_adb:
    logger.debug('  %s', d)
  logger.debug('Should reboot:')
  for d in should_reboot_device:
    logger.debug('  %s', d)

  if blacklist:
    blacklist.Reset()

  if should_restart_adb:
    KillAllAdb()
    adb_wrapper.AdbWrapper.StartServer()

  for serial in should_restart_usb:
    try:
      # TODO(crbug.com/642194): Resetting may be causing more harm
      # (specifically, kernel panics) than it does good.
      if enable_usb_reset:
        reset_usb.reset_android_usb(serial)
      else:
        logger.warning('USB reset disabled for %s (crbug.com/642914)',
                       serial)
    except IOError:
      logger.exception('Unable to reset USB for %s.', serial)
      if blacklist:
        blacklist.Extend([serial], reason='USB failure')
    except device_errors.DeviceUnreachableError:
      logger.exception('Unable to reset USB for %s.', serial)
      if blacklist:
        blacklist.Extend([serial], reason='offline')

  device_utils.DeviceUtils.parallel(devices).pMap(
      RecoverDevice, blacklist,
      should_reboot=lambda device: device.serial in should_reboot_device)


def main():
  parser = argparse.ArgumentParser()
  logging_common.AddLoggingArguments(parser)
  script_common.AddEnvironmentArguments(parser)
  parser.add_argument('--blacklist-file', help='Device blacklist JSON file.')
  parser.add_argument('--known-devices-file', action='append', default=[],
                      dest='known_devices_files',
                      help='Path to known device lists.')
  parser.add_argument('--enable-usb-reset', action='store_true',
                      help='Reset USB if necessary.')

  args = parser.parse_args()
  logging_common.InitializeLogging(args)
  script_common.InitializeEnvironment(args)

  blacklist = (device_blacklist.Blacklist(args.blacklist_file)
               if args.blacklist_file
               else None)

  expected_devices = device_status.GetExpectedDevices(args.known_devices_files)
  usb_devices = set(lsusb.get_android_devices())
  devices = [device_utils.DeviceUtils(s)
             for s in expected_devices.union(usb_devices)]

  RecoverDevices(devices, blacklist, enable_usb_reset=args.enable_usb_reset)


if __name__ == '__main__':
  sys.exit(main())
