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


class TestBootactionRenderAction(object):
    def test_bootaction_render_nodename(self, input_files, deckhand_ingester,
                                        setup):
        """Test the bootaction render routine provides expected output."""
        input_file = input_files.join("deckhand_fullsite.yaml")

        design_state = DrydockState()
        design_ref = "file://%s" % str(input_file)

        design_status, design_data = deckhand_ingester.ingest_data(
            design_state=design_state, design_ref=design_ref)

        ba = design_data.get_bootaction('helloworld')
        action_id = ulid2.generate_binary_ulid()
        assets = ba.render_assets('compute01', design_data, action_id,
                                  design_ref)

        assert 'compute01' in assets[0].rendered_bytes.decode('utf-8')

    def test_bootaction_render_design_ref(self, input_files, deckhand_ingester,
                                          setup):
        """Test the bootaction render routine provides expected output."""
        input_file = input_files.join("deckhand_fullsite.yaml")

        design_state = DrydockState()
        design_ref = "file://%s" % str(input_file)

        design_status, design_data = deckhand_ingester.ingest_data(
            design_state=design_state, design_ref=design_ref)

        ba = design_data.get_bootaction('helloworld')
        action_id = ulid2.generate_binary_ulid()
        assets = ba.render_assets('compute01', design_data, action_id,
                                  design_ref)

        assert 'deckhand_fullsite.yaml' in assets[2].rendered_bytes.decode(
            'utf-8')

    def test_bootaction_network_context(self, input_files,
                                        deckhand_orchestrator, setup):
        """Test that a boot action creates proper network context."""
        input_file = input_files.join("deckhand_fullsite.yaml")

        design_ref = "file://%s" % str(input_file)

        design_status, design_data = deckhand_orchestrator.get_effective_site(
            design_ref)

        ba = design_data.get_bootaction('helloworld')
        node = design_data.get_baremetal_node('compute01')
        net_ctx = ba.asset_list[0]._get_node_network_context(node, design_data)

        assert 'mgmt' in net_ctx
        assert net_ctx['mgmt'].get('ip', None) == '172.16.1.21'

    def test_bootaction_interface_context(self, input_files,
                                          deckhand_orchestrator, setup):
        """Test that a boot action creates proper network context."""
        input_file = input_files.join("deckhand_fullsite.yaml")

        design_ref = "file://%s" % str(input_file)

        design_status, design_data = deckhand_orchestrator.get_effective_site(
            design_ref)

        ba = design_data.get_bootaction('helloworld')
        node = design_data.get_baremetal_node('compute01')
        iface_ctx = ba.asset_list[0]._get_node_interface_context(node)

        assert 'bond0' in iface_ctx
        assert iface_ctx['bond0'].get('sriov')
        assert iface_ctx['bond0'].get('vf_count') == 2
