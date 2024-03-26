import json

import meraki


# Get the Meraki dashboard API key from the Kubernetes secrets.
with open('/var/openfaas/secrets/afarina-meraki-api-key', 'r') as file:
    MERAKI_API_KEY = file.read().rstrip()


def handle(serial_number: str) -> str:
    """
    Return the Meraki device's utilization (in percent).

    Args:
        serial_number (str): The serial number of the Meraki device.

    Returns:
        (str): The JSON-formatted string of the Meraki device's utilization
        (if successful). Otherwise, returns a failure message.
    """

    # Make the connection to the Meraki dashboard.
    meraki_dashboard = meraki.DashboardAPI(MERAKI_API_KEY, suppress_logging=True)

    # Send a request to get the Meraki device's utilization.
    device_utilization_response = meraki_dashboard.appliance.getDeviceAppliancePerformance(
        serial_number
    )

    # Return a response based off the response from the Meraki API.
    if device_utilization_response:
        return json.dumps({
            "status": "success",
            "cpu_usage": device_utilization_response.get('perfScore')
        })
    else:
        return json.dumps({
            "status": "failure",
            "reason": "Unexpected response from the Meraki API"
        })
