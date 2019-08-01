#!/usr/bin/env python
"""
Routines for extracting data from gnuplot.
"""
#######################
from __future__ import unicode_literals, print_function
#######################

import tempfile
import csv
import os
import subprocess


POSSIBLE_GNUPLOT = [
    '/usr/bin/gnuplot',
    '/usr/local/bin/gnuplot',
    '/Applications/Gnuplot.app/Contents/Resources/bin/gnuplot',
    '/Applications/local/Gnuplot.app/Contents/Resources/bin/gnuplot',
]



class Plot:

    def __init__(self, data=None, terminal=None, output_filename=None,
                 script=None):
        self.data = data
        self.terminal = terminal
        self.output_filename = output_filename
        self.script = script
        self._gnuplot_cmd = self.find_gnuplot()



    def _make_datafile(self):
        if self.data is None:
            return None
        datafile = tempfile.NamedTemporaryFile(mode='w+')
        dataWriter = csv.writer(datafile, delimiter=str('\t'), quotechar=str('"'),
                                quoting=csv.QUOTE_MINIMAL)
        for d in self.data:
            if hasattr(d, '__iter__'):
                dataWriter.writerow(d)
            else:
                dataWriter.writerow([d,])

        datafile.flush()
        return datafile


    def find_gnuplot(self):
        for f in POSSIBLE_GNUPLOT:
            if os.path.exists(f):
                return f


    def plot(self, wait=False, wait_prompt=None, debug=False, nodata_error=False):
        if not self._gnuplot_cmd:
            raise RuntimeError('self._gnuplot_cmd is not set!')
        datafile = self._make_datafile()
        if datafile is not None:
            script = self.script % {'datafile': datafile.name}
        else:
            script = self.script

        pre_script = 'reset\n'
        if self.terminal:
            pre_script += 'set terminal ' + self.terminal + '\n'

        if not self.output_filename:
            img_data = tempfile.NamedTemporaryFile()
            output_filename = img_data.name
        else:
            output_filename = self.output_filename
        if output_filename:
            pre_script += 'set output "%s"\n' % output_filename

        p = subprocess.Popen([self._gnuplot_cmd, ],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         universal_newlines=True)
        input = pre_script + script
        if debug:
            print("plot()::input = {input!r}".format(input=input))
        output, errors = p.communicate(input=input)
        if debug:
            print("plot()::output = {output!r}".format(output=output))
            print("plot()::errors = {errors!r}".format(errors=errors))

        if wait:
            if wait_prompt is None:
                input("Press ENTER to continue... ")
            else:
                input(wait_promt)

        if not self.output_filename:
            # read the file and return the data
            img_data.flush()
            img_data.seek(0)
            data = img_data.read()
            if not data and nodata_error:
                raise RuntimeError("plot():: no img_data returned!")
            return data
