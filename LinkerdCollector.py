# coding=utf-8

"""
Collects data from linkerd/admin/metrics.json

#### Dependencies

 * urllib2
 * json (or simeplejson)

"""

try:
    import json
except ImportError:
    import simplejson as json

import urllib2
import diamond.collector


class LinkerdCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(LinkerdCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(LinkerdCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': 9990,
            'uri': '/admin/metrics.json',
        })
        return config

    def collect(self):
        #
        # if there is a / in front remove it
        if self.config['uri'][0] == '/':
            self.config['uri'] = self.config['uri'][1:]

        try:
            response = urllib2.urlopen("http://%s:%s/%s" % (
                self.config['host'],
                int(self.config['port']),
                self.config['uri'])
            )
        except Exception, e:
            self.log.error('Couldnt connect to linkerd: %s', e)
            return {}

        try:
            j = json.loads(response.read())
        except Exception, e:
            self.log.error('Couldnt parse json: %s', e)
            return {}

        for k, v in j.items():
            k = k.replace(".", "_")
            k = k.replace("#", "")
            k = k.replace("//", "/")
            k = k.replace("/", ".")

            self.publish(k, v)
