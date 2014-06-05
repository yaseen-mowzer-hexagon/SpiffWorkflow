__author__ = 'matth'

import unittest
import os
from SpiffWorkflow.bpmn.parser.filters import EclipseConvertAbsolutePlatformImportsToRelativePaths

class EclipseConvertAbsolutePlatformImportsToRelativePathsTestCase(unittest.TestCase):

    def setUp(self):
        self.bpmn_test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        self.spiff_root_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        self.filter = EclipseConvertAbsolutePlatformImportsToRelativePaths({
                'platform:/resource/SpiffWorkflow' :
                self.spiff_root_dir,
            })

    def test_same_folder(self):
        converted, new_location = self.filter._convert_location(
            os.path.join(self.bpmn_test_data_dir, 'Dynamic-Loading-Workflows', 'level-01.bpmn'),
            'platform:/resource/SpiffWorkflow/tests/SpiffWorkflow/bpmn/data/Dynamic-Loading-Workflows/level-02-B.bpmn'
        )
        self.assertTrue(converted, 'Must be converted')
        self.assertEqual('level-02-B.bpmn', new_location)

    def test_link_to_parent_folder(self):
        converted, new_location = self.filter._convert_location(
            os.path.join(self.bpmn_test_data_dir, 'Dynamic-Loading-Workflows', 'level-01.bpmn'),
            'platform:/resource/SpiffWorkflow/tests/SpiffWorkflow/bpmn/data/level-02-B.bpmn'
        )
        self.assertTrue(converted, 'Must be converted')
        self.assertEqual('../level-02-B.bpmn', new_location)

    def test_link_to_grant_parent_folder(self):
        converted, new_location = self.filter._convert_location(
            os.path.join(self.bpmn_test_data_dir, 'Dynamic-Loading-Workflows', 'level-01.bpmn'),
            'platform:/resource/SpiffWorkflow/tests/SpiffWorkflow/bpmn/level-02-B.bpmn'
        )
        self.assertTrue(converted, 'Must be converted')
        self.assertEqual('../../level-02-B.bpmn', new_location)

    def test_link_from_parent_folder(self):
        converted, new_location = self.filter._convert_location(
            os.path.join(self.bpmn_test_data_dir, 'level-01.bpmn'),
            'platform:/resource/SpiffWorkflow/tests/SpiffWorkflow/bpmn/data/Dynamic-Loading-Workflows/level-02-B.bpmn'
        )
        self.assertTrue(converted, 'Must be converted')
        self.assertEqual('Dynamic-Loading-Workflows/level-02-B.bpmn', new_location)

    def test_link_from_grant_parent_folder(self):
        converted, new_location = self.filter._convert_location(
            os.path.abspath(os.path.join(self.bpmn_test_data_dir, '..', 'level-01.bpmn')),
            'platform:/resource/SpiffWorkflow/tests/SpiffWorkflow/bpmn/data/Dynamic-Loading-Workflows/level-02-B.bpmn'
        )
        self.assertTrue(converted, 'Must be converted')
        self.assertEqual('data/Dynamic-Loading-Workflows/level-02-B.bpmn', new_location)

    def test_link_to_root_folder(self):
        converted, new_location = self.filter._convert_location(
            os.path.join(self.bpmn_test_data_dir, 'Dynamic-Loading-Workflows', 'level-01.bpmn'),
            'platform:/resource/SpiffWorkflow/level-02-B.bpmn'
        )
        self.assertTrue(converted, 'Must be converted')
        self.assertEqual('../../../../../level-02-B.bpmn', new_location)

    def test_link_from_root_folder(self):
        converted, new_location = self.filter._convert_location(
            os.path.join(self.spiff_root_dir, 'level-01.bpmn'),
            'platform:/resource/SpiffWorkflow/tests/SpiffWorkflow/bpmn/data/Dynamic-Loading-Workflows/level-02-B.bpmn'
        )
        self.assertTrue(converted, 'Must be converted')
        self.assertEqual('tests/SpiffWorkflow/bpmn/data/Dynamic-Loading-Workflows/level-02-B.bpmn', new_location)

    def test_both_at_root_folder(self):
        converted, new_location = self.filter._convert_location(
            os.path.join(self.spiff_root_dir, 'level-01.bpmn'),
            'platform:/resource/SpiffWorkflow/level-02-B.bpmn'
        )
        self.assertTrue(converted, 'Must be converted')
        self.assertEqual('level-02-B.bpmn', new_location)