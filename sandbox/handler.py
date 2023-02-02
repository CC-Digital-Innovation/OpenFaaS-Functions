import json

secret_name = 'test-secret'
with open('/var/openfaas/secrets/' + secret_name, 'r') as file:
    data = file.read().rstrip()


def handle(req):
    """Handle a request to the function.

    Args:
        req (str): request body
    """
    new_data = json.loads(req)

    return json.dumps(
        {
            "object_given": json.dumps(new_data),
            secret_name: data
        }
    )
