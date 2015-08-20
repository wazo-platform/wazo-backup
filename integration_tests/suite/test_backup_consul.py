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

import json

from hamcrest import assert_that
from hamcrest import contains
from hamcrest import has_entries
from hamcrest import none

from base import BaseBackupIntegrationTest
from base import DEFAULT_TOKEN


RESTORE_DATA = json.dumps([
    "7",
    [
        {
            "CreateIndex": 7,
            "Flags": 42,
            "Key": "xivo/test",
            "LockIndex": 0,
            "ModifyIndex": 7,
            "Value": "test",
        }
    ]
])


class TestBackupConsul(BaseBackupIntegrationTest):

    asset = 'backup'

    def test_that_backing_up_dumps_the_keys(self):
        self.consul().kv.put('xivo/test', 'test')

        output = self.backup()

        result = json.loads(output)
        assert_that(result[1], contains(has_entries({'Key': 'xivo/test',
                                                     'Value': 'test'})))


class TestBackupRestoreConsul(BaseBackupIntegrationTest):

    asset = 'backup'

    def test_that_restoring_backed_up_kv_restore_consul_kv(self):
        self.consul().kv.put('xivo/test', 'test', flags=42)

        output = self.backup()

        self.consul().kv.delete('', recurse=True)
        result = self.consul().kv.get('xivo/test')
        assert_that(result[1], none())

        self.restore(output)

        result = self.consul().kv.get('xivo/test')
        assert_that(result[1], has_entries({'Key': 'xivo/test',
                                            'Value': 'test',
                                            'Flags': 42}))


class TestBackupRestoreConsulFile(BaseBackupIntegrationTest):

    asset = 'backup'

    def test_that_restoring_backed_up_kv_via_file_restore_consul_kv(self):
        self.consul().kv.put('xivo/test', 'test', flags=42)

        self.backup('-H consul -t {token} -o /var/tmp/consul_kv.json'.format(token=DEFAULT_TOKEN))

        self.consul().kv.delete('', recurse=True)
        result = self.consul().kv.get('xivo/test')
        assert_that(result[1], none())

        self.restore(input_=None, args='-H consul -t {token} -i /var/tmp/consul_kv.json'.format(token=DEFAULT_TOKEN))

        result = self.consul().kv.get('xivo/test')
        assert_that(result[1], has_entries({'Key': 'xivo/test',
                                            'Value': 'test',
                                            'Flags': 42}))


class TestBackupRestoreConsulTokenAuto(BaseBackupIntegrationTest):

    asset = 'token-auto'

    def test_that_backup_restore_find_token_in_file(self):
        self.consul(token='automatic_master_token').kv.put('xivo/test', 'test', flags=42)

        backup = self.backup('-H consul')

        self.consul(token='automatic_master_token').kv.delete('', recurse=True)
        result = self.consul(token='automatic_master_token').kv.get('xivo/test')
        assert_that(result[1], none())

        self.restore(backup, args='-H consul'.format(token=DEFAULT_TOKEN))

        result = self.consul(token='automatic_master_token').kv.get('xivo/test')
        assert_that(result[1], has_entries({'Key': 'xivo/test',
                                            'Value': 'test',
                                            'Flags': 42}))


class TestBackupConsulHostPortToken(BaseBackupIntegrationTest):

    asset = 'different-host-port-token'

    def test_that_host_port_options_are_used(self):
        self.consul(host='localhost', port=8501, token='the_other_token').kv.put('xivo/test', 'test')

        output = self.backup('-H consul-other-host -p 8501 -t the_other_token')

        result = json.loads(output)
        assert_that(result[1], contains(has_entries({'Key': 'xivo/test',
                                                     'Value': 'test'})))


class TestRestoreConsulHostPortToken(BaseBackupIntegrationTest):

    asset = 'different-host-port-token'

    def test_that_host_port_options_are_used(self):
        consul_args = {
            'host': 'localhost',
            'port': 8501,
            'token': 'the_other_token'
        }
        self.wait_for_consul(**consul_args)

        self.restore(RESTORE_DATA, args='-H consul-other-host -p 8501 -t the_other_token')

        result = self.consul(**consul_args).kv.get('xivo/test')
        assert_that(result[1], has_entries({'Key': 'xivo/test',
                                            'Value': 'test'}))
