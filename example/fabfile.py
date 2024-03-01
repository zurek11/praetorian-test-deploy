import os
import warnings

from dotenv import load_dotenv
from fabric import task
from praetorian_fabric.config import PraetorianConfig

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, '.env')

if os.path.exists(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE, verbose=True)

praetorian_config = PraetorianConfig(project_name='example')


@task
def deploy(ctx, remote_name):
    ctx = praetorian_config.connect(ctx, remote_name)

    ctx.run(f'mkdir {{{{ test_file1 }}}} {{{{ test_file2 }}}}')
    ctx.run('ls')
    ctx.run(f'rmdir {{{{ test_file1 }}}} {{{{ test_file2 }}}}')

    ctx.run(f'mkdir {{{{ test_file2 }}}} {{{{ test_file3 }}}}')
    ctx.run('ls')
    ctx.run(f'rmdir {{{{ test_file2 }}}} && rmdir {{{{ test_file3 }}}}')

    ctx.run('exit')

    return
