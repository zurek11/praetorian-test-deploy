import os
import warnings

from dotenv import load_dotenv
from fabric import Connection, task
from invoke import Context
from praetorian_api_client.api_client import ApiClient
from praetorian_api_client.configuration import Environment, Configuration

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, '.env')

PROJECT_NAME = 'diplomovka'

if os.path.exists(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE, verbose=True)


def _get_api_client(username: str, password: str) -> ApiClient:
    environment = Environment(name='praetorian-api', api_url=os.getenv('PRAETORIAN_API_URL'), read_only=False)
    configuration = Configuration(
        environment=environment, key=os.getenv('PRAETORIAN_API_KEY'), secret=os.getenv('PRAETORIAN_API_SECRET')
    )

    return ApiClient.create_from_auth(
        configuration=configuration,
        username=username,
        password=password
    )


def _get_configuration(api_client: ApiClient) -> dict:
    user = api_client.user.get_me()
    service = api_client.service.get(service_id=user.additional_data.get('service_id'))
    return service.variables


def _get_connection(ctx: Context, username: str, password: str) -> Connection:
    ctx.host = os.getenv('PROXY_HOST')
    ctx.port = int(os.getenv('PROXY_PORT'))

    ctx.user = username
    ctx.connect_kwargs.password = password

    ctx = Connection(
        host=ctx.host,
        user=ctx.user,
        port=ctx.port,
        connect_kwargs=ctx.connect_kwargs,
    )

    ctx.config['run']['echo'] = True
    return ctx


@task
def deploy(ctx, username, password):
    api_client = _get_api_client(username, password)
    config = _get_configuration(api_client)
    ctx = _get_connection(ctx, username, password)

    ctx.run(f'mkdir {{{{ test_file }}}}')
    ctx.run(f'ls {{{{ command }}}}')
    ctx.run(f'rmdir {{{{ test_file }}}}')

    ctx.run(f'mkdir {{{{ test_file1 }}}} {{{{ test_file2 }}}}')
    ctx.run(f'ls {{{{ command }}}}')
    ctx.run(f'exit')
    return
