# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import logging
import sys
import time


def AddLoggingArguments(parser):
  parser.add_argument(
      '-v', '--verbose', action='count', default=0,
      help='Log more. Use multiple times for even more logging.')


def InitializeLogging(args, handler=None):
  if args.verbose == 0:
    log_level = logging.WARNING
  elif args.verbose == 1:
    log_level = logging.INFO
  else:
    log_level = logging.DEBUG
  logger = logging.getLogger()
  logger.setLevel(log_level)
  if not handler:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CustomFormatter())
  logger.addHandler(handler)


class CustomFormatter(logging.Formatter):
  """Custom log formatter."""

  # override
  def __init__(self, fmt='%(threadName)-4s  %(message)s'):
    # Can't use super() because in older Python versions logging.Formatter does
    # not inherit from object.
    logging.Formatter.__init__(self, fmt=fmt)
    self._creation_time = time.time()

  # override
  def format(self, record):
    # Can't use super() because in older Python versions logging.Formatter does
    # not inherit from object.
    msg = logging.Formatter.format(self, record)
    if 'MainThread' in msg[:19]:
      msg = msg.replace('MainThread', 'Main', 1)
    timediff = time.time() - self._creation_time
    return '%s %8.3fs %s' % (record.levelname[0], timediff, msg)

