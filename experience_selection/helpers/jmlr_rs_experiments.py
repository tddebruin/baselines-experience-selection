import sys
import json

possible_env_arguments = {
    '-ipsu': 'RoboschoolInvertedPendulumSwingup-v1',
    '-ip': 'RoboschoolInvertedPendulum-v1',
    '-reacher': 'RoboschoolReacher-v1',
    '-idp': 'RoboschoolInvertedDoublePendulum-v1',
    '-ant': 'RoboschoolAnt-v1',
    '-hopper': 'RoboschoolHopper-v1',
    '-cheetah': 'RoboschoolHalfCheetah-v1',
    '-walker': 'RoboschoolWalker2d-v1'
}

decay_experiments = {
}

buffer_sizes = {
    'RoboschoolInvertedDoublePendulum-v1': ([1e6, 5e5, 3.18e5, 2e5, 1e5, 4e4],
                                               ['1m', '500k', '318k', '200k', '100k', '40k']),
    'RoboschoolReacher-v1': ([1e6, 2e5, 1e5, 4e4, 2.8e4, 2e4,  1e4],
                             ['1m', '200k', '100k', '40k', '28k', '20k', '10k']),
    'RoboschoolWalker2d-v1': ([1e6, 5e5, 2e5, 1.64e5, 1e5, 4e4],
                              ['1m', '500k','200k','164k', '100k', '40k']),
    'RoboschoolHalfCheetah-v1': ([1e6, 5e5, 2.64e5, 2e5,  1e5, 4e4],
                              ['1m', '500k', '264k', '200k', '100k', '40k']),
    'RoboschoolHopper-v1': ([1e6, 6.44e5, 5e5, 2e5, 1e5, 4e4],
                            ['1m', '644k', '500k','200k', '100k', '40k']),
    'RoboschoolAnt-v1': ([1e6, 7e5, 5e5, 2e5, 1e5, 4e4],
                                               ['1m', '700k', '500k','200k', '100k', '40k'])

}

if __name__ == '__main__':
    args = sys.argv[1:]

    experiments = []
    environments = []

    for arg in args:
        environments.append(possible_env_arguments[arg])
    if len(environments) == 0:
        environments = ['RoboschoolReacher-v1',
                        'RoboschoolAnt-v1',
                        'RoboschoolWalker2d-v1',
                        'RoboschoolHopper-v1',
                        'RoboschoolHalfCheetah-v1',
                        ]

    base_settings = {
        'project_dir': 'jmlr_es_rs',
        'noise-type': 'adaptive-param_0.2',
        'buffer_sample': 'uniform',
    }

    for env in environments:
        sizes = buffer_sizes.get(env, ([1e6, 5e5, 2e5, 1e5, 4e4],
                                               ['1m', '500k','200k', '100k', '40k']))
        for db_sze, db_sze_str in zip(*sizes):
            for ows in ['FIFO', 'expl_1.2', 'tde_1.2', 'resv']:
                if ows == 'FIFO' or db_sze < 1e6:
                    setting = base_settings.copy()
                    setting['env-id'] = env
                    setting['buffer_overwrite'] = ows
                    setting['buffer_size'] = db_sze
                    setting['experiment_name'] = '{:s}_{:s}'.format(db_sze_str, ows)
                    experiments.append(setting)

        if env in decay_experiments:
            decay_settings = decay_experiments[env]
            for ows in ['FIFO', 'expl_1.2', 'tde_1.2', 'resv', 'FULL']:
                setting = base_settings.copy()
                setting['env-id'] = env
                setting['buffer_overwrite'] = 'FIFO' if ows == 'FULL' else ows
                setting['final_exploration'] = 0.02
                if ows == 'FULL':
                    setting['buffer_size'] = 1e6
                    db_sze_str = '1m'
                else:
                    setting['buffer_size'] = decay_settings['db_sze']
                    db_sze_str = decay_settings['db_sze_str']
                setting['experiment_name'] = 'DECAY_{:s}_{:s}'.format(db_sze_str, ows)
                experiments.append(setting)

    with open('../../experiments_to_run.json', mode='w') as f:
        json.dump(experiments,f,indent=4)