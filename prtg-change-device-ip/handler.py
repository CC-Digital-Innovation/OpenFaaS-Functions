import json

import requests


def make_response(status: str, reason: str, status_code: int) -> str:
    """Create a JSON-formatted string response for the client.

    Args:
        status (str): The status of the response in words. Usually 'success'
        or 'failure'.
        reason (str): The reason for the status of this response.
        status_code (int): The HTTP status code related to the reason for
        the status of this response.

    Returns:
        The JSON-formatted response as a string.
    """
    return json.dumps(
        {
            'status': status,
            'reason': reason,
            'status_code': status_code
        }
    )


# Global constant response strings.
SUCCESSFUL_RESPONSE = make_response('success',
                                    'Successfully changed the device''s IP!',
                                    200)
INVALID_PAYLOAD_RESPONSE = make_response('failure',
                                         'Invalid payload provided.', 400)
INVALID_PRTG_INSTANCE_RESPONSE = make_response('failure',
                                               'Could not reach the PRTG '
                                               'instance.', 400)
UNABLE_TO_CHANGE_IP_RESPONSE = make_response('failure',
                                             'PRTG was unable to change the '
                                             'device''s IP.', 400)
UNAUTHORIZED_RESPONSE = make_response('failure',
                                      'You are not authorized to do this.', 401)


def handle(payload: str) -> str:
    """Given a JSON-formatted payload string, change a device's IP in PRTG.

    Args:
        payload (str): JSON payload string. Valid format:
        {
          "prtg_instance": <PRTG Instance URL>,
          "prtg_api_key": <PRTG API Key>,
          "prtg_device_id": <ID of Device in PRTG>,
          "new_device_ip": <The Device's New IP>
        }

    Returns:
        Response: The Response object from PRTG.
    """
    # Try to extract a JSON-formatted dictionary from the payload.
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return INVALID_PAYLOAD_RESPONSE
    else:
        # Check if the data object is not a dictionary.
        if type(data) is not dict:
            return INVALID_PAYLOAD_RESPONSE

    # Prepare variable to inspect the payload.
    has_valid_keys = 'prtg_instance' in data and 'prtg_api_key' in data and \
                     'prtg_device_id' in data and 'new_device_ip' in data

    # Check if the payload is invalid.
    if len(data) != 4 or not has_valid_keys:
        return INVALID_PAYLOAD_RESPONSE

    # Prepare variables to send the request to the PRTG API.
    prtg_api_call = f"{data.get('prtg_instance')}/api/setobjectproperty.htm"
    api_call_params = {
        'id': data.get('prtg_device_id'),
        'name': 'host',
        'value': data.get('new_device_ip'),
        'apitoken': data.get('prtg_api_key')
    }

    # Try to send the request to the PRTG API and capture the response.
    try:
        prtg_response = requests.get(url=prtg_api_call, params=api_call_params)
    except requests.exceptions.RequestException:
        return INVALID_PRTG_INSTANCE_RESPONSE
    else:
        # Check if the request failed on PRTG's end.
        if prtg_response.status_code == 401:
            return UNAUTHORIZED_RESPONSE
        elif prtg_response.status_code != 200:
            return UNABLE_TO_CHANGE_IP_RESPONSE

    # Return the successful response from PRTG.
    return SUCCESSFUL_RESPONSE
