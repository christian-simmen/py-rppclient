# Python RPP Client

RPP is still work in progress. For more information about the current progress please see:

* (IETF WG)[https://datatracker.ietf.org/group/rpp/about/]
* (RPP WG Github Organization)[https://github.com/ietf-wg-rpp]
* (RPP WG Wiki)[https://wiki.ietf.org/en/group/rpp]

This program was part of the (IETF 122 Hackathon)[https://wiki.ietf.org/en/group/rpp/rpp-hackathon]

## What to expect
* GET a domain object from a server
*

## What NOT to expect
For RPP is not fully defined most of the (requirements)[https://github.com/SIDN/ietf-wg-rpp-charter/blob/main/requirements.md] are not implemented yet.

## Usage

```bash
usage: py-rppclient.py [-h] [-s SERVER] [-d DOMAIN] [-i] [-v] {create,info,check,update,delete}

Python RPP Client

positional arguments:
  {create,info,check,update,delete}
                        Operation to perform

options:
  -h, --help            show this help message and exit
  -s, --server SERVER   Base URL of the Server API
  -d, --domain DOMAIN   Domainname
  -i, --interactive     Interactive template expansion
  -v, --verbose         Verbose mode

```

## Examples
```bash
# create example.de
./py-rppclient.py create --base_url "http://127.0.0.1:8000" --domain_id example.de -i

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
