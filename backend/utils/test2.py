#!/usr/bin/env python
# coding: utf8

import os
import rancher
import requests


class RancherHTTPRequest:
    def __init__(self):
        # self._RANCHER_API_ENDPOINT = os.getenv('RANCHER_API_ENDPOINT')
        # self._RANCHER_API_TOKEN = os.getenv("CATTLE_ACCESS_KEY")
        # self._RANCHER_API_KEY = os.getenv("CATTLE_SECRET_KEY")
        self._RANCHER_API_ENDPOINT = 'https://rancher888.com/v3'
        self._RANCHER_API_TOKEN = 'token-j9nbd'
        self._RANCHER_API_KEY = 'lkhdjz6s889tbqx74xq7cdlm6qxjlmpczxdrmktjmd5r8jw64482f4'

    def makeRequest(self, suffix):
        req = requests.get(self._RANCHER_API_ENDPOINT + '/projects' + suffix,
                           headers={'Content-Type': 'application/json'},
                           auth=(self._RANCHER_API_TOKEN, self._RANCHER_API_KEY),
                           )
        print(req)
        json_ = req.json()
        return json_


class RancherAPI:
    def __init__(self):
        self._projectId = 'c-nc96c:p-4gfvs'
        self._requester = RancherHTTPRequest()
        self._PROJECT_SUFFIX = '/%s/projects' % self._projectId
        self._ALLSTACKS_SUFFIX = '/%s/projects/%s/stacks' % (self._projectId, self._projectId)
        self._ALLSERVICES_SUFFIX = lambda stack: '/%s/stacks/%s/services' % (self._projectId, stack)
        self._ALLCONTAINERS_SUFFIX = lambda serviceid: '/%s/services/%s/instances' % (self._projectId, serviceid)

    @property
    def requester(self):
        return self._requester

    @property
    def projectId(self):
        return self._projectId

    def _makeLinksRequest(self, suffix):
        json_ = self._requester.makeRequest(suffix)
        links = json_.get('data')[0].get('links')
        return links

    def _makeDataRequest(self, suffix):
        json_ = self._requester.makeRequest(suffix)
        return json_.get('data')

    def getProject(self):
        return self._makeLinksRequest(self._PROJECT_SUFFIX)

    def getAllStacks(self):
        return self._makeDataRequest(self._ALLSTACKS_SUFFIX)

    def getAllServices(self, stack):
        return self._makeDataRequest(self._ALLSERVICES_SUFFIX(stack))

    def getAllContainers(self, serviceid):
        return self._makeDataRequest(self._ALLCONTAINERS_SUFFIX(serviceid))

if __name__ == '__main__':
    rr = RancherAPI()
    d = rr.getProject()
    print(d)