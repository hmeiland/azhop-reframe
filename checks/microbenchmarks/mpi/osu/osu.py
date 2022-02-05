import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class AlltoallTest(rfm.RunOnlyRegressionTest):
    strict_check = False
    valid_systems = ['*']
    descr = 'Alltoall OSU microbenchmark'
    executable = 'osu_alltoall'
    # The -m option sets the maximum message size
    # The -x option sets the number of warm-up iterations
    # The -i option sets the number of iterations
    executable_opts = ['-m', '8', '-x', '1000', '-i', '20000']
    valid_prog_environs = ['*',]
    modules = ['OSU-Micro-Benchmarks/5.6.3-gompi-2020a']
    maintainers = ['HM']
    reference = {
        'dom:gpu': {
            'latency': (8.23, None, 0.1, 'us')
        },
        'daint:gpu': {
            'latency': (20.73, None, 2.0, 'us')
        }
    }
    num_tasks = 16 
    num_tasks_per_node = 8
    num_cpus_per_task = 4 

    @sanity_function
    def assert_found_8byte_latency(self):
        return sn.assert_found(r'^8', self.stdout)

    @run_before('performance')
    def set_performance_patterns(self):
        self.perf_patterns = {
            'latency': sn.extractsingle(r'^8\s+(?P<latency>\S+)',
                                        self.stdout, 'latency', float)
        }

@rfm.simple_test
class BandwidthTest(rfm.RunOnlyRegressionTest):
    strict_check = False
    valid_systems = ['*']
    descr = 'Bandwidth OSU microbenchmark'
    executable = 'osu_bw'
    # The -m option sets the maximum message size
    # The -x option sets the number of warm-up iterations
    # The -i option sets the number of iterations
    executable_opts = ['-x', '1000', '-i', '20000']
    valid_prog_environs = ['*',]
    modules = ['OSU-Micro-Benchmarks/5.6.3-gompi-2020a']
    maintainers = ['HM']
    reference = {
        'dom:gpu': {
            'latency': (8.23, None, 0.1, 'us')
        },
        'daint:gpu': {
            'latency': (20.73, None, 2.0, 'us')
        }
    }
    num_tasks = 2
    num_tasks_per_node = 1
    # num_cpus_per_task = 44
    time_limit = 3600 

    @run_before('run')
    def set_hostfile(self):
        self.job.launcher.options = ['--hostfile $PBS_NODEFILE --map-by ppr:1:node --path $PATH']

    @sanity_function
    def assert_found_4MB_bandwidth(self):
        return sn.assert_found(r'^4194304', self.stdout)

    @performance_function('MB/s')
    def bandwidth(self):
        return sn.extractsingle(r'^4194304\s+(\S+)',
                                self.stdout, 1, float)
