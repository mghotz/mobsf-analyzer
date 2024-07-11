import os
import time
from .redis_client import RedisClient
from .mobsf_client import MobSFClient

class APKProcessor:
    def __init__(self, redis_client, mobsf_client, queue_name, results_key_base):
        self.redis_client = redis_client
        self.mobsf_client = mobsf_client
        self.queue_name = queue_name
        self.results_key_base = results_key_base

    def process_apk(self, apk_path):
        print(f"Processing APK: {apk_path}")
        upload_response = self.mobsf_client.upload_apk(apk_path)
        if upload_response is not None:
            print(f"Upload response: {upload_response}")
            hash_value = upload_response.get('hash')
            if hash_value:
                scan_results = self.mobsf_client.scan_apk(hash_value)
                if scan_results:
                    results_key = f"{self.results_key_base}:{os.path.basename(apk_path)}"
                    self.redis_client.save_results(results_key, scan_results)
                    print(f"Results saved for {apk_path}")
                else:
                    print(f"Failed to scan APK: {apk_path}")
            else:
                print(f"Upload response missing hash for APK: {apk_path}")
        else:
            print(f"Failed to upload APK: {apk_path}")

    def run(self):
        print("Starting APKProcessor...")
        while True:
            apk_data = self.redis_client.get_from_queue(self.queue_name)
            if apk_data:
                apk_path = apk_data[1].decode('utf-8')
                print(f"Received APK from queue: {apk_path}")
                self.process_apk(apk_path)
            else:
                print("No APK in queue, waiting...")
                time.sleep(5)
