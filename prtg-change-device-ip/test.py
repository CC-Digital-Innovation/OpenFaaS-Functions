from handler import *

import os
import unittest


class TestPRTGChangeDeviceIP(unittest.TestCase):
    """Test the OpenFaaS function on the development instance of PRTG"""
    def setUp(self):
        """Make a valid testing payload for each test to reference or alter."""
        self.testing_payload_dict = {
            'prtg_api_key': os.environ.get('PRTG_DEV_INST_API_TOKEN'),
            'prtg_instance': os.environ.get('PRTG_DEV_INST_URL'),
            'prtg_device_id': '40',
            'new_device_ip': '127.0.0.1'
        }

    def test_function_success(self):
        """Test the success of the function with a valid payload."""
        valid_payload = json.dumps(self.testing_payload_dict)
        self.assertEqual(handle(valid_payload), SUCCESSFUL_RESPONSE)

    def test_invalid_payload_too_long(self):
        """Test the function when passed an invalid payload with more than
        the 4 expected key-value pairs."""
        # Long payload with all valid key-value pairs inside it.
        self.testing_payload_dict['five'] = 5
        long_payload = json.dumps(self.testing_payload_dict)
        self.assertEqual(handle(long_payload), INVALID_PAYLOAD_RESPONSE)

        # Long payload with no valid key-value pairs inside it.
        long_invalid_payload = json.dumps({
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5
        })
        self.assertEqual(handle(long_invalid_payload), INVALID_PAYLOAD_RESPONSE)

    def test_invalid_payload_too_short(self):
        """Test the function when passed an invalid payload with less than
        the 4 expected key-value pairs."""
        # Short payload with 1 less valid key-value pair inside it.
        self.testing_payload_dict = self.testing_payload_dict.pop(
            'prtg_api_key')
        short_payload = json.dumps(self.testing_payload_dict)
        self.assertEqual(handle(short_payload), INVALID_PAYLOAD_RESPONSE)

        # Short payload with just 1 invalid key-value pair inside it.
        one_kv_payload = json.dumps({'one': 1})
        self.assertEqual(handle(one_kv_payload), INVALID_PAYLOAD_RESPONSE)

    def test_invalid_payload_not_a_dictionary(self):
        """Test the function when passed an invalid payload that is not in a
        JSON-formatted dictionary."""
        # Non-dictionary formatted string.
        self.assertEqual(handle('Not a dictionary!'), INVALID_PAYLOAD_RESPONSE)

        # Empty string.
        self.assertEqual(handle(''), INVALID_PAYLOAD_RESPONSE)

        # Digit string.
        self.assertEqual(handle('1'), INVALID_PAYLOAD_RESPONSE)

    def test_invalid_api_key(self):
        """Test the function with an invalid API key."""
        # Alter the valid PRTG API key.
        self.testing_payload_dict['prtg_api_key'] = 'invalid-key'
        invalid_api_key_payload = json.dumps(self.testing_payload_dict)
        self.assertEqual(handle(invalid_api_key_payload), UNAUTHORIZED_RESPONSE)

    def test_invalid_prtg_instance(self):
        """Test the function with an invalid PRTG instance URL."""
        # Alter the valid PRTG instance URL.
        self.testing_payload_dict['prtg_instance'] = 'notvalid.prtginstance'
        invalid_prtg_instance_payload = json.dumps(self.testing_payload_dict)
        self.assertEqual(handle(invalid_prtg_instance_payload),
                         INVALID_PRTG_INSTANCE_RESPONSE)

    def test_invalid_ids(self):
        """Test the function with various types of invalid IDs."""
        # Use a non-existent ID.
        self.testing_payload_dict['prtg_device_id'] = '99999999'
        nonexistent_id_payload = json.dumps(self.testing_payload_dict)
        self.assertEqual(handle(nonexistent_id_payload),
                         UNABLE_TO_CHANGE_IP_RESPONSE)

        # Use an invalid ID (NAN).
        self.testing_payload_dict['prtg_device_id'] = 'invalid'
        invalid_id_payload = json.dumps(self.testing_payload_dict)
        self.assertEqual(handle(invalid_id_payload),
                         UNABLE_TO_CHANGE_IP_RESPONSE)

        # Use an empty ID.
        self.testing_payload_dict['prtg_device_id'] = ''
        empty_id_payload = json.dumps(self.testing_payload_dict)
        self.assertEqual(handle(empty_id_payload), UNABLE_TO_CHANGE_IP_RESPONSE)


if __name__ == '__main__':
    unittest.main()
