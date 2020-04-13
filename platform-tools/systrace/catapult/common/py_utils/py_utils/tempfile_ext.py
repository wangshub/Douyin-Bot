# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


import contextlib
import shutil
import tempfile


@contextlib.contextmanager
def NamedTemporaryDirectory(suffix='', prefix='tmp', dir=None):
  """A context manager that manages a temporary directory.

  This is a context manager version of tempfile.mkdtemp. The arguments to this
  function are the same as the arguments for that one.

  This can be used to automatically manage the lifetime of a temporary file
  without maintaining an open file handle on it. Doing so can be useful in
  scenarios where a parent process calls a child process to create a temporary
  file and then does something with the resulting file.
  """
  # This uses |dir| as a parameter name for consistency with mkdtemp.
  # pylint: disable=redefined-builtin

  d = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
  try:
    yield d
  finally:
    shutil.rmtree(d)
