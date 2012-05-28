from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib import files
from time import gmtime, strftime

debug = True

PROJECT = 'cartvine'
PROJECT_PATH = '/home/rossc/Projects/Personal/%s' % (PROJECT,)
PROJECT_DEPLOY_INSTANCE = ( ('cartvine_app', 'cartvine'), ('cartvine_shoppers', 'facebook_user'),)

REMOTE_PROJECT_PATHS = []
for project,app in PROJECT_DEPLOY_INSTANCE:
  REMOTE_PROJECT_PATHS.append( (project, app, '/home/stard0g101/webapps/%s' % (project)) )

live_hosts = ('stard0g101@stard0g101.webfactional.com')

FILENAME_TIMESTAMP = strftime("%m-%d-%Y-%H:%M:%S", gmtime())


@hosts(['localhost'])
def git_export():
  cd(PROJECT_PATH)
  local('git archive --format zip --output /tmp/%s.zip --prefix=%s/ master'%(PROJECT,PROJECT,), capture=False)


def prepare_deploy():
    git_export()
    put('/tmp/'+ PROJECT +'.zip', '/tmp/')


def deploy(env, project_name, app_name, remote_project_path):
    # extract project zip file
    with cd('%s/'%(remote_project_path,)):
      run('unzip /tmp/%s.zip'%(PROJECT,))
      run('unlink /tmp/%s.zip'%(PROJECT,))
      cd( '%s/%s'%(remote_project_path, project_name,))
      run('cp %s/%s/conf/%s/%s.local_settings.py %s/%s/%s/local_settings.py'%(remote_project_path,app_name,project_name,env, remote_project_path,project_name,app_name,))
      run('rm -Rf %s/%s/media'%(remote_project_path,project_name,))
      run('rm -Rf %s/%s/static'%(remote_project_path,project_name,))
      run('%s/apache2/bin/restart'%(remote_project_path,))


@hosts(live_hosts)
def deploy_live():
  env = 'live'
  prepare_deploy()
  for project, app_name, project_path in REMOTE_PROJECT_PATHS:
    deploy(env, project, app_name, project_path)
