```markdown
# MobSF APK Processor

This project automates the processing of APK files using MobSF (Mobile Security Framework). It uploads APK files to MobSF, triggers a scan, and saves the results to Redis.

## Features

- Automatically process APK files from a Redis queue.
- Upload APK files to MobSF.
- Trigger a static analysis scan in MobSF.
- Save the scan results to Redis.

## Prerequisites

- Python 3.x
- Redis
- MobSF (Mobile Security Framework)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mghotz/mobsf-analyzer.git
   cd mobsf-apk-processor
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Redis and MobSF are running on your localhost.

## Configuration

Update the following configurations in your project as needed:

- `MobSFClient`: Update the `mobsf_url` and `api_key` in `mobsf_client.py` to point to your MobSF instance.
- `RedisClient`: Adjust Redis configurations if needed in `redis_client.py`.

## Usage

### Running the APK Processor

To start the APK processor, run the following command:

```bash
python main.py
```

### Adding APKs to the Queue

You can add APK files to the Redis queue manually using a Python script:

```python
from app.redis_client import RedisClient

def add_apk_to_queue(apk_path):
    redis_client = RedisClient(host='localhost', port=6379, db=0)
    queue_name = 'apk_queue'
    redis_client.add_to_queue(queue_name, apk_path)
    print(f"Added {apk_path} to {queue_name}")

if __name__ == '__main__':
    apk_path = 'path/to/your/apk/file.apk'
    add_apk_to_queue(apk_path)
```

### Checking the Results

After processing, the results are stored in Redis. You can check the results using the provided `check_redis.py` script:

```bash
python check_redis.py
```

### Running Tests

This project includes tests written with `pytest`. To run the tests:

```bash
pytest tests/
```

## Project Structure

```
mob_sf_processor/
├── app/
│   ├── __init__.py
│   ├── process_apk.py
│   ├── redis_client.py
│   └── mobsf_client.py
├── tests/
│   ├── __init__.py
│   └── test_process_apk.py
├── requirements.txt
└── main.py
```

- **app/process_apk.py**: Contains the `APKProcessor` class that handles the APK processing workflow.
- **app/redis_client.py**: Handles interactions with Redis.
- **app/mobsf_client.py**: Manages communication with the MobSF API.
- **tests/**: Contains unit tests for the project.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```
