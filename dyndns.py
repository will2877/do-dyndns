#!/usr/bin/python3
import argparse
import requests
import json

"""
Copyright (c) 2021 William Ihde <william@ihde.ch>
"""


# Load the parameters
def load_paramertes():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=True, help="Location of the Configuration file")
    ap.add_argument("-l", "--list", action='store_true', required=False, help="List all domains", )
    return vars(ap.parse_args())


# Load the application config from the file that was specified in the arguments.
def load_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)


# Load the IP address of the
def get_my_ip():
    r = requests.get("https://ipconfig.io/json")
    if r.status_code != 200:
        raise RuntimeError(f"Got bad status code from http request {r.status_code}")
    return json.loads(r.text)


# Get a list of all Domains that are available under the current that fits the accesstoken.
def list_domains(headers):
    domains_request = requests.get("https://api.digitalocean.com/v2/domains", headers=headers)

    if domains_request.status_code != 200:
        raise RuntimeError(f"Got status code {domains_request.status_code} from Domains API")
    domains = json.loads(domains_request.text)

    for domain in domains['domains']:
        url = f"https://api.digitalocean.com/v2/domains/{domain['name']}/records"
        record_request = requests.get(url, headers=headers)

        if record_request.status_code != 200:
            raise RuntimeError(
                f"Got status code {record_request.status_code} from Records API for the domain {domain['name']}")

        records = json.loads(record_request.text)

        print(f"{domain['name']}")

        for record in records['domain_records']:
            print(f"{record['id']}: {record['type']} {record['name']} {record['data']}")
        print("------------------------------------------------------")


def update_record(record, ip, headers):
    # Get the current state
    url = f"https://api.digitalocean.com/v2/domains/{record['domain']}/records/{record['id']}"
    current_state = requests.get(url, headers=headers)

    if current_state.status_code != 200:
        error = json.loads(current_state.text)
        raise RuntimeError(
            f"Got status code {current_state.status_code} from Records API for the domain {record['domain']} and ID {record['id']} Message: {error['message']}")

    current = json.loads(current_state.text)['domain_record']

    # compare it to my current IP
    if current['data'] != ip:
        # Update the new IP
        print(f"Updating IP! Old: {current['data']} New: {ip} ")
        update_result = requests.put(url, params={'data': ip}, headers=headers)
    else:
        print(f"The IP {ip} is upto date for the host \"{current['name']}\" of the domain \"{record['domain']}\"!")


if __name__ == '__main__':
    args = load_paramertes() # Get Parameters
    try:
        config = load_config(args['config'])
    except json.decoder.JSONDecodeError as jsonError:
        print("Config or Request contained bad JSON")
        print(jsonError)
    except RuntimeError as requestError:
        print(requestError)

    else:
        # Headers for DigitalOcean this will allow us to authenticate against DigitalOcean
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(config["api_key"])}

        # Check if we need to List the available record
        if args["list"]:
            try:
                list_domains(headers)
            except RuntimeError as error:
                print(error)
                exit(1)
            else:
                exit(0)

        # Query our current IP
        ip = get_my_ip()

        # Update the records where required.
        for record in config['records']:
            try:
                update_record(record, ip['ip'], headers)
            except RuntimeError as error:
                print(error)