import requests
import urllib
import urlparse

from st2actions.runners.pythonrunner import Action

class ActiveCampaignAction(Action):

    
    def run(self, **kwargs):
        if kwargs['api_key'] is None:
            kwargs['api_key'] = self.config['api_key']

        return self._get_request(kwargs)

    def _get_request(self, params):
        url = urlparse.urljoin(self.config['url'], 'admin/api.php')
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        params = self._format_params(params)
        data = urllib.urlencode(params)
        self.logger.info(data)
        response = requests.get(url=url,
                                headers=headers, params=data)

        results = response.json()
        if not results['ok']:
            failure_reason = ('Failed to perform action %s: %s \
                              (status code: %s)' % (end_point, response.text,
                              response.status_code))
            self.logger.exception(failure_reason)
            raise Exception(failure_reason)

        return results

    def _format_params(self, params):
        output = {}
        for k, v in params.iteritems():
            if isinstance(v, object):
                for pk, pv in v.iteritems():
                    param_name = "%s[%s]" % (k, pk)
                    output[param_name] = pv
             else:
                 output[k] = v
        return output
