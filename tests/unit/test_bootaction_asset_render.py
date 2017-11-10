# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test that boot action assets are rendered correctly."""

import ulid2

from drydock_provisioner.statemgmt.state import DrydockState
import drydock_provisioner.objects as objects


class TestClass(object):
    def test_bootaction_render(self, input_files, deckhand_ingester, setup):
        objects.register_all()

        input_file = input_files.join("deckhand_fullsite.yaml")

        design_state = DrydockState()
        design_ref = "file://%s" % str(input_file)

        design_status, design_data = deckhand_ingester.ingest_data(
            design_state=design_state, design_ref=design_ref)

        ba = design_data.get_bootaction('helloworld')
        action_id = ulid2.generate_binary_ulid()
        assets = ba.render_assets('compute01', design_data, action_id)

        assert 'compute01' in assets[0].rendered_bytes.decode('utf-8')
