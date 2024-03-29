from django.conf import settings
from django.contrib.auth.models import User
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils.encoding import smart_str, smart_unicode

import os
import time
import subprocess

COMPRESSOR = getattr(settings, 'COMPRESSOR_PATH', '../yuicompressor-2.4.7.jar')

PRECOMPRESSED_TARGET_FILES = [
]
COMPRESSOR_TARGET_FILES = [
    '%s/cartvine/apps/default%shandlebars.js'%(settings.SITE_ROOT, settings.STATIC_URL),
    '%s/cartvine/apps/default%sleviroutes.js'%(settings.SITE_ROOT, settings.STATIC_URL),
]

PRECOMPRESSED_TARGET_FILES = getattr(settings, 'PRECOMPRESSED_TARGET_FILES', PRECOMPRESSED_TARGET_FILES)
COMPRESSOR_TARGET_FILES = getattr(settings, 'COMPRESSOR_TARGET_FILES', COMPRESSOR_TARGET_FILES)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
      make_option('--target', dest='target_file', default='cartvine/apps/default/static/cartvine-complete.js',
      help='The target output file relative to settings.SITE_ROOT default: cartvine/apps/default/static/cartvine-complete.js'),
      make_option('--dont-output', dest='no_output', default=False,
      help='Dont output to stdout the final complete file'),
    )

    target = None
    tmp_target = None
    
    def handle(self, **options):
        """ Command uses YUI compressor to combine various js/css files 
        into one file
        """
        no_output = options.get('no_output')
        target_file = options.get('target_file')

        self.target = '%s/%s' % (settings.SITE_ROOT, target_file)
        self.tmp_target = '%s.tmp' %(self.target,)

        for f in PRECOMPRESSED_TARGET_FILES:
          if os.path.exists(f):
            self.append_file(f)
          else:
            raise Exception('File to Compress does not exist. The file specified (%s) Does not exist'%(f,))

        for f in COMPRESSOR_TARGET_FILES:
          if os.path.exists(f):
            self.compress_file(f)
          else:
            raise Exception('File to Compress does not exist. The file specified (%s) Does not exist'%(f,))

        self.finalize()

        if not no_output:
          self.output()


    def finalize(self):
      # remove "old" original target file
      if os.path.exists(self.tmp_target):
        os.remove(self.target)

      # output the tmp file to the primary file
      cmd = '/bin/cat %s > %s' % (self.tmp_target, self.target)
      os.system(cmd)

      # delete tmp file assuming the required file now exists
      if os.path.exists(self.target):
        os.remove(self.tmp_target)

    def output(self):
      cmd = '/bin/cat %s' % (self.target,)
      os.system(cmd)

    def append_file(self, source_file):
      cmd = '/bin/cat %s >> %s' % (source_file, self.tmp_target)
      #cmd = '/bin/cat %s' % (source_file,)
      os.system(cmd)

    def compress_file(self, source_file):
      cmd = '/usr/bin/java -jar %s/%s %s >> %s' % (settings.SITE_ROOT, COMPRESSOR, source_file, self.tmp_target)
      os.system(cmd)
