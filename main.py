from app.redis_client import RedisClient
from app.mobsf_client import MobSFClient
from app.process_apk import APKProcessor

def main():
    redis_client = RedisClient(host='localhost', port=6379, db=1)
    mobsf_client = MobSFClient(mobsf_url='http://localhost:8000', api_key='e748ff40bc3d4bc34731541f2df44768dd37bec262033fc7e100de29e142a364')
    apk_processor = APKProcessor(redis_client, mobsf_client, queue_name='apk_queue', results_key_base='apk_results')

    apk_processor.run()

if __name__ == '__main__':
    main()

