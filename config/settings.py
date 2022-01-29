site_configuration = {
    'systems': [
        {
            'name': 'azhop',
            'descr': 'Azure HPC Ondemand with PBS',
            'modules_system': 'lmod',
	        'hostnames': ['ondemand'],
            'partitions': [
                {
                    'name': 'hc44rs',
                    'scheduler': 'pbs',
                    'access': ['slot_type=hc44rs'],
                    'launcher': 'local',
                    'modules': ['foss/2020a'],
                    'environs': ['builtin'],
                    'processor': {
                        'num_cpus': 44,
                    },
                    'descr': 'HC44rs Skylake vm'
                },
                {
                    'name': 'hb120v2',
                    'scheduler': 'pbs',
                    'access': ['slot_type=hb120v2'],
                    'launcher': 'local',
                    'modules': ['foss/2020a'],
                    'environs': ['builtin'],
                    'processor': {
                        'num_cpus': 120,
                    },
                    'descr': 'HB120v2 Rome vm'
                },
                {
                    'name': 'hb120v3',
                    'scheduler': 'pbs',
                    'access': ['slot_type=hb120v3'],
                    'launcher': 'local',
                    'modules': ['foss/2020a'],
                    'environs': ['builtin'],
                    'processor': {
                        'num_cpus': 120,
                    },
                    'descr': 'HB120v3 Milan vm'
                },
             ]
         },
     ],
    'environments': [
        {
            'name': 'builtin',
            'cc': 'gcc',
            'cxx': '',
            'ftn': '',
        },
     ],
     'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'name': 'reframe.log',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',   # noqa: E501
                    'append': False
                }
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_info)s|jobid=%(check_jobid)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'append': True
                }
            ]
        }
    ],
}
