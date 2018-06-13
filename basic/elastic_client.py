# -*- coding: utf-8 -*-
import json
import requests


class ElasticClient:

    def __init__(self, host, port, user, pwd):
        self.session = requests.Session()
        self.headers = {'Connection': 'Keep-Alive'}
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd

    def get_health(self):
        try:
            url = '%s/%s' % (self.__server(), "_cluster/health")
            result = self.session.get(url, auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None



    # https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html
    def index(self, index, type, id, query):
        try:
            url = '%s/%s/%s/%s' % (self.__server(), index, type, id)
            result = self.session.put(url, json.dumps(query), auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None

    # https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html
    def get(self, index, type, id):
        try:
            url = '%s/%s/%s/%s' % (self.__server(), index, type, id)
            result = self.session.get(url, auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None

    # https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html
    def delete(self, index, type, id):
        try:
            url = '%s/%s/%s/%s' % (self.__server(), index, type, id)
            result = self.session.delete(url, auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None

    # https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html
    def create_index(self, index, shards, replicas):
        try:
            query = {
                'settings': {
                    'index': {
                        'number_of_shards': shards,
                        'number_of_replicas': replicas
                    }
                }
            }
            url = '%s/%s/' % (self.__server(), index)
            result = self.session.put(url, json.dumps(query), auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None

    # https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-delete-index.html
    def delete_index(self, index):
        try:
            url = '%s/%s/' % (self.__server(), index)
            result = self.session.delete(url, auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None

    def isIndexExist(self, index):
        try:
            url = '%s/%s/' % (self.__server(), index)
            result = self.session.head(url, auth=(self.user, self.pwd), headers=self.headers)
            if result.status_code == 200:
                return True
            else:
                return False
        except:
            return None

    def put_mapping(self, index, type, query):
        try:
            url = '%s/%s/_mapping/%s' % (self.__server(), index, type)
            result = self.session.put(url, json.dumps(query), auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None

    def post_script(self, scriptId, query):
        try:
            url = '%s/_scripts/painless/%s' % (self.__server(), scriptId)
            result = self.session.post(url, json.dumps(query), auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None

    def exclude_allocation_ip(self, index, ipList):
        try:
            url = '%s/%s/_settings' % (self.__server(), index)
            query = {
                "index.routing.allocation.exclude._ip": ipList
            }
            result = self.session.put(url, json.dumps(query), auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None

    # method = 'post'/'get'/'put'/'delete'
    def do_something_to_somewhere(self, method, somewhere, something):
        try:
            url = '%s/%s' % (self.__server(), somewhere)
            result = self.session.request(method, url, data=json.dumps(something), auth=(self.user, self.pwd), headers=self.headers)
            return result.content
        except:
            return None

    def __server(self):
        return 'http://%s:%s' % (self.host, self.port)
