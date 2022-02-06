# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class StreamTest(rfm.RegressionTest):
    '''This test checks the stream test:
       Function    Best Rate MB/s  Avg time     Min time     Max time
       Triad:          13991.7     0.017174     0.017153     0.017192
    '''

    def __init__(self):
        self.descr = 'STREAM Benchmark'
        self.exclusive_access = True
        self.valid_systems = ['*']
        self.valid_prog_environs = ['eessi-foss-2020a']
        self.modules = ['foss/2020a']

        self.use_multithreading = False

        self.prgenv_flags = {
            'builtin': ['-fopenmp', '-O3'],
            #'eessi-foss-2020a': ['-fopenmp', '-O', '-DSTREAM_ARRAY_SIZE=20000000'],
            'eessi-foss-2020a': ['-Ofast', '-DSTREAM_ARRAY_SIZE=100000000', '-DNTIMES=20', '-fopenmp', '-mcmodel=medium'],
        }

        self.sourcepath = 'stream.c'
        self.build_system = 'SingleSource'
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.stream_cpus_per_task = {
            'azhop:hc44rs': 44,
            'azhop:hb120v2': 120,
            'azhop:hb120v3': 120,
        }
        self.variables = {
            'OMP_PLACES': 'cores',
            'OMP_PROC_BIND': 'close'
        }
        self.sanity_patterns = sn.assert_found(
            r'Solution Validates: avg error less than', self.stdout)
        self.perf_patterns = {
            'triad': sn.extractsingle(r'Triad:\s+(?P<triad>\S+)\s+\S+',
                                      self.stdout, 'triad', float)
        }
        self.stream_bw_reference = {
            'eessi-foss-2020a': {
                'azhop:hc44rs': {'triad': (10000, -0.05, None, 'MB/s')},
                'azhop:hb120v2': {'triad': (20000, -0.05, None, 'MB/s')},
                'azhop:hb120v3': {'triad': (30000, -0.05, None, 'MB/s')},
            },
        }
        self.tags = {'production', 'azhop'}
        self.maintainers = ['HM']

    @run_after('setup')
    def prepare_test(self):
        self.num_cpus_per_task = self.stream_cpus_per_task.get(
            self.current_partition.fullname, 1)
        #self.variables['OMP_NUM_THREADS'] = str(self.num_cpus_per_task)
        self.job.launcher.options = ['--map-by node:PE='+str(self.num_cpus_per_task)]
        envname = self.current_environ.name

        self.build_system.cflags = self.prgenv_flags.get(envname, ['-O3'])

        try:
            self.reference = self.stream_bw_reference[envname]
        except KeyError:
            self.reference = self.stream_bw_reference['builtin']
