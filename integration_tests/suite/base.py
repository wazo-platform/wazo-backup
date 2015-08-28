# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
import os
import subprocess
import time
import unittest

from consul import Consul
from consul import ConsulException
from hamcrest import assert_that
from hamcrest import none

logger = logging.getLogger(__name__)
ASSETS_ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets')

DEFAULT_TOKEN = 'the_one_ring'
DEFAULT_CONSUL_ARGS = {
    'host': 'localhost',
    'port': 8500,
    'token': DEFAULT_TOKEN
}


class BaseBackupIntegrationTest(unittest.TestCase):

    oldpwd = None

    @classmethod
    def launch_sync_with_asset(cls):
        cls.container_name = cls.asset
        asset_path = os.path.join(ASSETS_ROOT, cls.asset)
        cls.oldpwd = os.getcwd()
        os.chdir(asset_path)
        cls._run_cmd('docker-compose rm --force')
        cls._run_cmd('docker-compose run --rm sync')
        cls.wait_for_consul(**cls.consul_args)  # consul may still be busy electing himself...

    @classmethod
    def wait_for_consul(cls, **kwargs):
        for _ in xrange(10):
            try:
                Consul(**kwargs).kv.get('fullybooted')
                return
            except ConsulException:
                time.sleep(.5)
        else:
            Consul(**kwargs).kv.get('fullybooted')

    @classmethod
    def stop_with_asset(cls):
        cls._run_cmd('docker-compose kill')
        os.chdir(cls.oldpwd)

    @staticmethod
    def _run_cmd(cmd, input_=None):
        process = subprocess.Popen(cmd.split(' '),
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        out, _ = process.communicate(input_)
        logger.info(out)
        return out

    @classmethod
    def setUpClass(cls):
        cls.launch_sync_with_asset()

    @classmethod
    def tearDownClass(cls):
        cls.stop_with_asset()

    @classmethod
    def backup(cls, args=''):
        args = args or '-H consul -t {token}'.format(token=DEFAULT_TOKEN)
        backup_command = 'python xivo-backup-consul-kv {args}'.format(args=args)
        return cls._run_cmd('docker-compose run --rm backup {command}'.format(command=backup_command))

    @classmethod
    def restore(cls, input_, args=''):
        args = args or '-H consul -t {token}'.format(token=DEFAULT_TOKEN)
        restore_command = 'python xivo-restore-consul-kv {args}'.format(args=args)
        return cls._run_cmd('docker-compose run --rm backup {command}'.format(command=restore_command),
                            input_=input_)

    @classmethod
    def clear_consul(cls):
        cls.consul().kv.delete('', recurse=True)
        result = cls.consul().kv.get('', recurse=True)
        assert_that(result[1], none())

    @classmethod
    def consul(cls, **kwargs):
        consul_args = dict(cls.consul_args)
        consul_args.update(kwargs)
        return Consul(**consul_args)
