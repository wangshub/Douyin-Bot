#!/usr/bin/env python

# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import hashlib
import json
import os
import unittest

from systrace import decorators
from systrace import output_generator
from systrace import trace_result
from systrace import update_systrace_trace_viewer
from systrace import util
from tracing.trace_data import trace_data as trace_data_module


TEST_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
ATRACE_DATA = os.path.join(TEST_DIR, 'atrace_data')
BATTOR_DATA = os.path.join(TEST_DIR, 'battor_test_data.txt')
COMBINED_PROFILE_CHROME_DATA = os.path.join(
    TEST_DIR, 'profile-chrome_systrace_perf_chrome_data')


class OutputGeneratorTest(unittest.TestCase):

  @decorators.HostOnlyTest
  def testJsonTraceMerging(self):
    update_systrace_trace_viewer.update(force_update=True)
    self.assertTrue(os.path.exists(
        update_systrace_trace_viewer.SYSTRACE_TRACE_VIEWER_HTML_FILE))
    t1 = "{'traceEvents': [{'ts': 123, 'ph': 'b'}]}"
    t2 = "{'traceEvents': [], 'stackFrames': ['blah']}"
    results = [trace_result.TraceResult('a', t1),
               trace_result.TraceResult('b', t2)]

    merged_results = output_generator.MergeTraceResultsIfNeeded(results)
    for r in merged_results:
      if r.source_name == 'a':
        self.assertEquals(r.raw_data, t1)
      elif r.source_name == 'b':
        self.assertEquals(r.raw_data, t2)
    self.assertEquals(len(merged_results), len(results))
    os.remove(update_systrace_trace_viewer.SYSTRACE_TRACE_VIEWER_HTML_FILE)

  @decorators.HostOnlyTest
  def testHtmlOutputGenerationFormatsSingleTrace(self):
    update_systrace_trace_viewer.update(force_update=True)
    self.assertTrue(os.path.exists(
        update_systrace_trace_viewer.SYSTRACE_TRACE_VIEWER_HTML_FILE))
    with open(ATRACE_DATA) as f:
      atrace_data = f.read().replace(" ", "").strip()
      trace_results = [trace_result.TraceResult('systemTraceEvents',
                       atrace_data)]
      output_file_name = util.generate_random_filename_for_test()
      final_path = output_generator.GenerateHTMLOutput(trace_results,
                                                       output_file_name)
      with open(output_file_name, 'r') as f:
        output_generator.GenerateHTMLOutput(trace_results, f.name)
        html_output = f.read()
        trace_data = (html_output.split(
          '<script class="trace-data" type="application/text">')[1].split(
          '</script>'))[0].replace(" ", "").strip()
      os.remove(final_path)

    # Ensure the trace data written in HTML is located within the
    # correct place in the HTML document and that the data is not
    # malformed.
    self.assertEquals(trace_data, atrace_data)
    os.remove(update_systrace_trace_viewer.SYSTRACE_TRACE_VIEWER_HTML_FILE)

  @decorators.HostOnlyTest
  def testHtmlOutputGenerationFormatsMultipleTraces(self):
    trace_results = []
    trace_data_builder = trace_data_module.TraceDataBuilder()

    with open(BATTOR_DATA) as fp:
      battor_data = fp.read()
    trace_results.append(
        trace_result.TraceResult('powerTraceAsString', battor_data))
    trace_data_builder.AddTraceFor(
        trace_data_module.BATTOR_TRACE_PART, battor_data)

    with open(ATRACE_DATA) as fp:
      atrace_data = fp.read()
    trace_results.append(
        trace_result.TraceResult('systemTraceEvents', atrace_data))
    trace_data_builder.AddTraceFor(trace_data_module.ATRACE_PART, atrace_data)


    with open(COMBINED_PROFILE_CHROME_DATA) as fp:
      chrome_data = fp.read()
    trace_results.append(
        trace_result.TraceResult('traceEvents', json.loads(chrome_data)))
    trace_data_builder.AddTraceFor(
        trace_data_module.CHROME_TRACE_PART, json.loads(chrome_data))

    trace_results.append(
        trace_result.TraceResult('systraceController', str({})))
    trace_data_builder.AddTraceFor(trace_data_module.TELEMETRY_PART, {})

    try:
      data_builder_out = util.generate_random_filename_for_test()
      output_generator_out = util.generate_random_filename_for_test()
      output_generator.GenerateHTMLOutput(trace_results, output_generator_out)
      trace_data_builder.AsData().Serialize(data_builder_out, 'Systrace')

      output_generator_md5sum = hashlib.md5(
          open(output_generator_out, 'rb').read()).hexdigest()
      data_builder_md5sum = hashlib.md5(
          open(data_builder_out, 'rb').read()).hexdigest()

      self.assertEqual(output_generator_md5sum, data_builder_md5sum)
    finally:
      def del_if_exist(path):
        try:
          os.remove(path)
        except IOError:
          pass
      del_if_exist(output_generator_out)
      del_if_exist(data_builder_out)
