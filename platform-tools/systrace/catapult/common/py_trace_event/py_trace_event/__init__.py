# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
import os
import sys

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
PY_UTILS = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', 'py_utils'))
sys.path.append(PY_UTILS)
