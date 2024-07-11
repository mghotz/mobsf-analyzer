import redis
import json

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=1):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def add_to_queue(self, queue_name, apk_path):
        self.client.rpush(queue_name, apk_path)

    def get_from_queue(self, queue_name):
        return self.client.blpop(queue_name, timeout=0)

    def save_results(self, results_key, results):
        results_json = json.dumps(results)
        self.client.set(results_key, results_json)
