import json

import meraki


# Get the Meraki dashboard API key from the Kubernetes secrets.
with open('/var/openfaas/secrets/afarina-meraki-api-key', 'r') as file:
    MERAKI_API_KEY = file.read().rstrip()


def handle(serial_num: str):
    """Return the CPU usage (in percent) of a Meraki device.

    Args:
        serial_num (str): The serial number of the device.
    """

    # Make the connection to the Meraki dashboard.
    meraki_dash = meraki.DashboardAPI(MERAKI_API_KEY, suppress_logging=True)

    # Send the API request.
    response = meraki_dash.appliance.getDeviceAppliancePerformance(
        serial_num
    )

    # Return the response.
    if response:
        return json.dumps({
            "status": "success",
            "cpu_usage": response.get('perfScore')
        })
    else:
        return json.dumps({
            "status": "failure",
            "reason": "Unexpected response from the Meraki API"
        })
