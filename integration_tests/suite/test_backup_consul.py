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

from base import BaseBackupIntegrationTest


class TestBackupConsul(BaseBackupIntegrationTest):

    asset = 'backup'

    def test_that_backing_up_dumps_the_keys(self):
        self.consul().kv.put('xivo/test', 'test')

        output = self.backup()

        result = json.loads(output)
        assert_that(result[1], contains(has_entries({'Key': 'xivo/test',
                                                     'Value': 'test'})))


class TestBackupConsulHostPortToken(BaseBackupIntegrationTest):

    asset = 'different-host-port-token'

    def test_that_host_port_options_are_used(self):
        self.consul(host='localhost', port=8501, token='the_other_token').kv.put('xivo/test', 'test')

        output = self.backup('-H consul-other-host -p 8501 -t the_other_token')

        result = json.loads(output)
        assert_that(result[1], contains(has_entries({'Key': 'xivo/test',
                                                     'Value': 'test'})))
