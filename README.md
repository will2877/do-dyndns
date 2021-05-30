# DigitalOcean DynDNS

This is a simple script that acts as a DynDNS-Client for DigitalOcean, designed for home users that don't want to invest in a "propper" (whatever that is) DynDNS provider.
It is based on [this](https://gitlab.no/rune/dyndns) node nodejs solution, with the difference that it only dose IPv4 at the moment.

To run it, you need to create a copy of the `config.json` and replace the `api_key` with your own:
````bash
cp config.json config_local.json
vi config_local.json
chmod +x dyndns.py
````
The API key ca be created in the "API" Section of the DigitalOcean backend.

> IMPORTANT: When using it for the first time, you need to determine the `id` of the record that you would like.
> This can be done by calling the script with the `--list` parameter: `./dyndns.py --config config_local.json --list`  
> This will give you a List of all the records, IDs and their value.


The API URLs are taken from the [DigitalOcean Documentation](https://developers.digitalocean.com/documentation/v2/#domains)




