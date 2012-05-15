from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files
from time import gmtime, strftime

debug = True

PROJECT = 'shop_happy'
PROJECT_PATH = '/home/rossc/Projects/Personal/%s' % (PROJECT,)
REMOTE_PROJECT_PATH = '/home/stard0g101/webapps/%s' % (PROJECT,)

live_hosts = ('stard0g101@stard0g101.webfactional.com')

FILENAME_TIMESTAMP = strftime("%m-%d-%Y-%H:%M:%S", gmtime())


@hosts(['localhost'])
def git_export():
  cd(PROJECT_PATH)
  local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ master'%(PROJECT,PROJECT,), capture=False)


def prepare_deploy():
    git_export()


def deploy(env='staging', remote_project_path=None):
    if remote_project_path == None:
      remote_project_path = REMOTE_PROJECT_PATH

    prepare_deploy()

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
  remote_project_path = REMOTE_PROJECT_PATH
  deploy(env, remote_project_path)
