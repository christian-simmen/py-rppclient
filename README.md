# Python RPP Client

## Usage

```bash
usage: py-rppclient.py [-h] -s SERVER [-d DOMAIN] {fetch,create,info,check,update,delete}

Python RPP Client

positional arguments:
  {fetch,create,info,check,update,delete}
                        Operation to perform

options:
  -h, --help            show this help message and exit
  -s, --server SERVER   Base URL of the Server API
  -d, --domain DOMAIN   Domain (required for info, check, update, and delete operations)
```

## Examples
```bash
# fetch existing domains
./py-rppclient.py fetch --base_url "http://127.0.0.1:8000"
# fetch,create,get,update,delete
# create example.de
./py-rppclient.py create --base_url "http://127.0.0.1:8000" --domain_id example.de

# Domain INFO example.de
./py-rppclient.py info --base_url "http://127.0.0.1:8000" --domain_id example.de

# DOMAIN CHECK example.de
./py-rppclient.py check --base_url "http://127.0.0.1:8000" --domain_id example.de

# update example.de
./py-rppclient.py update --base_url "http://127.0.0.1:8000" --domain_id example.de

# delete example.de
./py-rppclient.py delete --base_url "http://127.0.0.1:8000" --domain_id example.de
```

## Set up a Server
see https://github.com/SIDN/ietf-rpp-api/tree/pawelk/dev/rpp_server_python_connexion
