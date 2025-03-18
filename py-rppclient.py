#!/usr/bin/python3

import requests
import json
from argparse import ArgumentParser

OPT_VERBOSE = False

class RPPDataObject():
  def __init__(self, obj_type, **kvargs):
    self.template_registry = {
        'internal': {
          'domain': 'models/internal/domain.json',
          'contact': 'models/internal/contact.json',
          'host': 'models/inernal/host.json',
          },
        'rpp': {
          'domain': 'models/rpp/domain.json',
          'contact': 'models/rpp/contact.json',
          'host': 'models/rpp/host.json',
        }
      }


    self.rpp_data_model = load_data_model(self.template_registry['rpp'][obj_type])
    self.data = load_data_model(self.template_registry['internal'][obj_type])
    if kvargs:
      self.set_data(**kvargs)

  def get_data(self):
    return self.data

  def set_data(self, **kvargs):
    for k, v in kvargs.items():
      self.data[k] = v

  def __get_input(self, reference, value):
    # assuming value is of the type we want to add
    # e.g. 'string', ['string1', 'string2'], {'key1': 'string', 'key2', ['string1', 'string2']}
    # FIXME: separate functions for str,dict,list
    vprint("ask for {}, old value {}".format(reference, value))
    if type(value) in (str, int, float):
      user_input = input("{}({}):".format(reference, value))

    elif type(value) == dict:
      # iterate over sub-elements
      user_input = {}
      if input("Add element '{}' (Y/n)".format(reference)).lower() not in ('n', 'no'):
        for k, v in value.items():
          next_input = self.__get_input("{}->{}".format(reference, k), v)
          if next_input:
            user_input[k] = next_input

    elif type(value) == list:
      user_input = []
      for i in range(1,10):
        if type(value[0]) not in (str, int, float):
          if input("Add element '{}' (Y/n)".format(reference)).lower() in ('n', 'no'):
            break
        next_input = self.__get_input("{}->{}".format(reference, i), value[0])
        if next_input:
          user_input.append(next_input)
        else:
          break

    else:
      print("Error: data type '{}' of '{}' is not supported yet")

    if user_input:
      return user_input
    return None

  def set_data_interactive(self):
    for k, v in self.data.items():
      user_input = self.__get_input(k, v)
      if user_input:
        self.data[k] = user_input
    vprint("------- saved data -------")
    vprint(json.dumps(self.data, indent=2))
    vprint("------- saved data -------")


  def get_rpp_data(self):
    for k, v in self.data.items():
      self.rpp_data_model[k] = v

    for k, v in self.rpp_data_model.items():
      if type(self.rpp_data_model[k]) == str and self.rpp_data_model[k] == "string":
        self.rpp_data_model[k] = ""
    return self.rpp_data_model



class RppClient():
  def __init__(self):
    self.args = None
    self.parse_args()

  def parse_args(self):
    parser = ArgumentParser(description='Python RPP Client')
    parser.add_argument('operation', help='Operation to perform', choices=['create', 'info', 'check', 'update', 'delete'])
    parser.add_argument('-s', '--server', help='Base URL of the Server API', required=False, default='http://127.0.0.1:8000')
    parser.add_argument('-d', '--domain', help='Domainname')
    parser.add_argument('-i', '--interactive', help='Interactive template expansion', action='store_true')
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')
    #parser.add_argument('-f' '--file', default=None, required=False, help='JSON file containing the payload (required for create and update operations)')
    self.args = parser.parse_args()

    if self.args.verbose:
      global OPT_VERBOSE
      OPT_VERBOSE = True

  def check_args(self):
    # FIXME: currently ony domains, need to be fixed when implementing contacts or ...
    if self.args.operation in ['create', 'info', 'check', 'update', 'delete']:
      if not self.args.domain:
        print('Error: --domain is required for Domain ' + str(self.args.operation).upper() + ' operation')
        return False
    return True

  def process_request(self):
    if not self.check_args():
      return False
    if self.args.operation == 'create':
      self.domain_create(domain=self.args.domain)

    elif self.args.operation == 'info':
      self.domain_info(domain=self.args.domain)

    elif self.args.operation == 'check':
      self.domain_check(domain=self.args.domain)

    elif self.args.operation == 'update':
      self.domain_update(domain=self.args.domain)

    elif self.args.operation == 'delete':
      self.domain_delete(domain=self.args.domain)

  def domain_create(self, domain=None):
    if domain:
      print('--- Domain CREATE (' + str(domain) + ') ---')
      domain = RPPDataObject("domain", name=domain)
      if self.args.interactive:
        domain.set_data_interactive()
      else:
        domain.set_data(name=domain)

      domain_data = domain.get_rpp_data()
      if domain_data:
        print(json.dumps(domain_data, indent=2))
        print(self._make_request('POST', '/domains', json=domain_data))

  def domain_info(self, domain=None):
    if domain:
      print('--- Domain INFO (' + str(domain) + ') ---')
      print(self._make_request('GET', '/domains/' + domain))

  def domain_check(self, domain=None):
    if domain:
      print('--- Domain INFO (' + str(domain) + ') ---')
      print(self._make_request('HEAD', '/domains/' + domain))

  def domain_update(self, domain=None):
    if domain:
      print('--- Domain INFO (' + str(domain) + ') ---')
      print(self._make_request('PATCH', '/domains/' + domain))

  def domain_delete(self, domain=None):
    if domain:
      print('--- Domain INFO (' + str(domain) + ') ---')
      print(self._make_request('DELETE', '/domains/' + domain))

  def _make_request(self, method=None, endpoint=None, **kwargs):
    try:
      print('Request: ' + method + ' ' + f'{self.args.server}{endpoint}')
      response = requests.request(method, f'{self.args.server}{endpoint}', **kwargs)
      response.raise_for_status()
      print('Response:\n' + str(response.headers) + '\n---\n' + str(response.content))
      return response.json() if response.content else {'message': 'Success'}
    except requests.exceptions.RequestException as e:
      print(f'Error: {e}')
      return None


def load_data_model(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f'Error loading payload: {e}')
        return None

def vprint(message):
  if OPT_VERBOSE:
    print(message)

if __name__ == '__main__':
  rpp = RppClient()
  vprint('\n-------------------------------------------------------------------------------------------------------------------\n'
        + str(rpp.args)
        + '\n-------------------------------------------------------------------------------------------------------------------'
    )
  rpp.process_request()
