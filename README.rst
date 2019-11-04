Garpun API Client
=================

|build| |pypi|

This library simplifies using Garpun's various server-to-server authentication
mechanisms to access Garpun APIs.


.. |build| image:: https://travis-ci.org/garpun/garpun-api-python-client.svg?branch=master
   :target: https://travis-ci.org/garpun/garpun-api-python-client
.. |pypi| image:: https://img.shields.io/pypi/v/garpunapiclient.svg
   :target: https://pypi.python.org/pypi/garpunapiclient


Installing
__________

You can install using `pip`_::

    $ pip install garpunapiclient

.. _pip: https://pip.pypa.io/en/stable/


Supported Python Versions
_________________________
Python >= 3.6


Using
_____


.. code-block:: python

    # Use it for first auth with your scopes
    from garpunapiclient.client import GarpunCredentials

    credentials, project_id = GarpunCredentials.authenticate_user(['cloud-platform'])

    print(u"credentials.access_token = %s" % str(credentials.access_token))
    print(u"credentials.access_token_expired = %s" % str(credentials.access_token_expired))
    print(u"credentials.refresh_token = %s" % str(credentials.refresh_token))

    # Refresh access_token if it expired
    GarpunCredentials.refresh_credentials(credentials)

    print(u"credentials.access_token = %s" % str(credentials.access_token))


For contributors
________________


1. Use `make blacken` for blacken the code
2. Use `nox` for run tests and other checks
3. Set PyCharm default test runner to pytest
