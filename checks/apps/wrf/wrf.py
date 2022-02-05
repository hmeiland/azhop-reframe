import os
import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.udeps as udeps

@rfm.simple_test
class WrfConusDownload(rfm.RunOnlyRegressionTest):
    descr = 'WRF benchmarks download Conus'
    valid_systems = ['azhop:execute']
    valid_prog_environs = ['builtin']
    executable = 'wget'
    keep_stage_files = 'true'
    executable_opts = [
        'http://www2.mmm.ucar.edu/wrf/bench/conus12km_v3911/bench_12km.tar.bz2'
    ]
    postrun_cmds = [
        'bunzip2 bench_12km.tar.bz2',
        'tar -xf bench_12km.tar'
    ]

    @sanity_function
    def validate_download(self):
        return sn.assert_true(os.path.exists('bench_12km'))



@rfm.simple_test
class WrfCheck(rfm.RunOnlyRegressionTest):
    descr = 'WRF benchmark Conus 12km'
    valid_systems = ['*']
    valid_prog_environs = ['eessi-foss-2020a']
    modules = ['WRF/3.9.1.1-foss-2020a-dmpar']
    executable = 'wrf.exe'
    keep_stage_files = 'true'

    @run_after('init')
    def inject_dependencies(self):
        self.depends_on('WrfConusDownload', how=udeps.fully)

    @require_deps
    def set_sourcedir(self, WrfConusDownload):
        self.sourcesdir = WrfConusDownload(part='execute', environ='builtin').stagedir

        self.readonly_files = ['bench_12km']
        self.prerun_cmds = [
            f'ln -s `dirname $(which wrf.exe)`/../run/* .',
            f'rm namelist.input',
            f'ln -s bench_12km/* .',
            f'rm rsl.*',
        ]
        self.num_tasks = 44 
        self.num_tasks_per_node = 44 

    @sanity_function
    def validate_test(self):
        return sn.assert_found(r'SUCCESS COMPLETE WRF', 'rsl.out.0000')

    @performance_function('sec')
    def bandwidth(self):
        return sn.extractsingle(r'/^Timing for main: time 2001-10-24_11:58:48 on domain   1:\s+(?P<latency>\S+)/gm',
                'rsl.out.0000', 1, float)
