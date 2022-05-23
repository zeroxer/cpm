import argparse
from multiprocessing import cpu_count
from pathlib import Path
import os
import sys
import shutil
import configparser
import time

config = configparser.ConfigParser()


parser = argparse.ArgumentParser(description='Qingo Libiary Manage Tool')
parser.add_argument('project_dir', type=str, help='Project location')
parser.add_argument('cmd', type=str, help='Command type name')

args = parser.parse_args()

target_location = args.project_dir
cmd_type = args.cmd

lib_root_dir = os.path.dirname(os.path.abspath(__file__))
project_location_abs = lib_root_dir + '/./' + target_location
if Path(target_location).is_dir():
    os.chdir(target_location)
else:
    print('Project location invalid!')
    exit(0)

# 进入到Project目录中: 目录中必须有.config文件
config.read('.config')
project_name = config['Common']['ProjectName']

project_root_dir = os.path.abspath(os.path.curdir)
# print('PM> Project Dir: {}'.format(project_root_dir))

project_build_dir = project_root_dir + '/.Build'
binary_file_dir = project_root_dir + '/export/bin/Debug'
binary_file_path = binary_file_dir + '/' + project_name + 'Test.exe'

# 多线程🧬选项
if sys.platform == 'win32':
    multithread_flag = '/m /nologo'
else:
    import multiprocessing
    cpu_count = max(1, multiprocessing.cpu_count() - 2)
    multithread_flag = '-j {}'.format(cpu_count)

if cmd_type == 'build':
    print('Start build debug library')
    Path('./.Build').mkdir(parents=True, exist_ok=True)
    generate_cmd = 'cmake -S {} -B {}'.format(project_root_dir, project_build_dir)
    build_cmd = 'cmake --build {} --config Debug -- {}'.format(project_build_dir, multithread_flag)
    # 统计时间
    start_time = time.time()
    os.system(generate_cmd)
    os.system(build_cmd)
    end_time = time.time()
    time_used = '%.2f' % (end_time - start_time)
    print('[PM]> Build finished.')
    print('[PM]> Time used: {}s.'.format(time_used))
elif cmd_type == 'publish':
    print('Start build debug library')
    Path('./.Build').mkdir(parents=True, exist_ok=True)
    generate_cmd = 'cmake -S {} -B {}'.format(project_root_dir, project_build_dir)
    build_cmd = 'cmake --build {} --config Release -- /m /nologo'.format(project_build_dir)
    os.system(generate_cmd)
    os.system(build_cmd)
elif cmd_type == 'run':
    run_cmd = 'call ' + binary_file_path
    print('PM> {}'.format(run_cmd))
    os.system(run_cmd)
elif cmd_type == 'clean':
    print('=> Start clean .Build dir.')
    if Path(project_build_dir).is_dir():
        shutil.rmtree(project_build_dir)
    else:
        # print('=> .Build is not a dir.')
        pass
    print('=> Finished clean .Build dir: {}'.format(project_build_dir))
elif cmd_type == 'debug':
    debug_cmd = 'start {}/{}.sln'.format(project_build_dir, project_name)
    os.system(debug_cmd)
else:
    print('Unknow cmd.')
