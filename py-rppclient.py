#!/usr/bin/python3


import requests
#import argparse
from argparse import ArgumentParser

import json


class RppClient():
  def __init__(self):
    self.args = None
    self.parse_args()

  def parse_args(self):
    parser = ArgumentParser(description='Python RPP Client')
    parser.add_argument('operation', choices=['create', 'info', 'check', 'update', 'delete'], help='Operation to perform')
    parser.add_argument('-s', '--server', required=True, help='Base URL of the Server API', default='http://127.0.0.1:8000')
    parser.add_argument('-d', '--domain', help='Domain (required for info, check, update, and delete operations)')
    #parser.add_argument('-f' '--file', default=None, required=False, help='JSON file containing the payload (required for create and update operations)')
    self.args = parser.parse_args()

  def check_args(self):
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
      domain_data = load_data_model('examples/json/domain/domain.json')
      if domain_data:
        domain_data['name'] = domain
        print(domain_data)
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

if __name__ == '__main__':
  rpp = RppClient()
  print('\n-------------------------------------------------------------------------------------------------------------------\n'
        + str(rpp.args)
        + '\n-------------------------------------------------------------------------------------------------------------------'
    )
  rpp.process_request()
