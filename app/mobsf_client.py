import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class MobSFClient:
    def __init__(self, mobsf_url, api_key):
        self.mobsf_url = mobsf_url
        self.api_key = api_key

    def upload_apk(self, apk_path):
        url = f"{self.mobsf_url}/api/v1/upload"
        headers = {
            'Authorization': self.api_key
        }
        try:
            with open(apk_path, 'rb') as apk_file:
                m = MultipartEncoder(fields={'file': ('filename.apk', apk_file, 'application/vnd.android.package-archive')})
                headers['Content-Type'] = m.content_type
                response = requests.post(url, data=m, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return None

    def scan_apk(self, hash_value):
        url = f"{self.mobsf_url}/api/v1/scan"
        headers = {
            'Authorization': self.api_key
        }
        data = {
            'hash': hash_value,
            're_scan': '0'
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.content}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return None
