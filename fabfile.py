from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files
from time import gmtime, strftime

debug = True

PROJECT = 'shop_happy'
PROJECT_PATH = '/home/rossc/Projects/Personal/%s' % (PROJECT,)
PROJECT_DEPLOY_INSTANCE = ('cartvine_app', 'cartvine_shoppers',)

REMOTE_PROJECT_PATHS = []
for p in PROJECT_DEPLOY_INSTANCE:
  REMOTE_PROJECT_PATHS.append('/home/stard0g101/webapps/%s' % (p))

live_hosts = ('stard0g101@stard0g101.webfactional.com')

FILENAME_TIMESTAMP = strftime("%m-%d-%Y-%H:%M:%S", gmtime())


@hosts(['localhost'])
def git_export():
  cd(PROJECT_PATH)
  local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ master'%(PROJECT,PROJECT,), capture=False)


def prepare_deploy():
    git_export()


def deploy(env, remote_project_path):
    put('/tmp/'+ PROJECT +'.zip', '/tmp/')

    # extract tar file
    with cd('%s/'%(remote_project_path,)):
      run('unzip /tmp/%s.zip'%(PROJECT,))
      cd( '%s/%s'%(remote_project_path, PROJECT,))
      run('cp %s/%s/conf/%s.local_settings.py %s/%s/%s/local_settings.py'%(remote_project_path,PROJECT,env,remote_project_path,PROJECT,PROJECT,))
      run('rm -Rf %s/%s/media'%(remote_project_path,PROJECT,))
      run('rm -Rf %s/%s/static'%(remote_project_path,PROJECT,))
      run(remote_project_path +'/apache2/bin/restart')

    run('unlink /tmp/%s.zip'%(PROJECT,)) 


@hosts(live_hosts)
def deploy_live():
  env = 'live'
  prepare_deploy()
  for project_path in REMOTE_PROJECT_PATHS:
    deploy(env, project_path)
