import yaml
import time
import requests
from collections import defaultdict

# parse url and name information from yaml file
def get_data_from_file(url:str):
    with open(url, 'r') as file:
        yaml_info = yaml.safe_load(file)

    name_url_map = defaultdict(list)
    for endpoint in yaml_info:
        name = endpoint['name'].split(' ')[0]
        url = endpoint['url']
        name_url_map[name].append(url)
    
    return name_url_map

# send get requests to all the endpoints
def send_requests(name_url_map: defaultdict, availability_map: dict):
    for url_name in name_url_map:
        for url in name_url_map[url_name]:
            
            try:
                r = requests.head(url)
                status_code = r.status_code
                response_time = r.elapsed.total_seconds()

                up = 0
                if 200 <= status_code <= 299 and response_time <= 0.5:
                    up = 1
            except:
                up = 0

            if url_name not in availability_map:
                availability_map[url_name] = [up, 1, up]
            else:
                up_count, total_count, _ = availability_map[url_name]
                availability_map[url_name][0] = up_count+up
                availability_map[url_name][1] = total_count+1
                availability_map[url_name][2] = (up_count+up) / (total_count+1)

# main function here, send HTTP requests every 15 seconds and log results
# change the file path variable to use a different YAML file
# change the pause_time to modify the re-send requests time
def main():
    file_path = 'sample_input.yaml'
    pause_time = 0.1
    name_url_map = get_data_from_file(file_path)
    availability_map = {}
    logs = []
    while(True):
        log = []
        send_requests(name_url_map, availability_map)

        for url_name in availability_map:
            percentage = round(availability_map[url_name][-1] * 100)
            str = f'{url_name} has {percentage}% availability percentage'
            log.append(str)
            print(str)
        logs.append(log)
        time.sleep(pause_time)

if __name__ == "__main__":
    main()
