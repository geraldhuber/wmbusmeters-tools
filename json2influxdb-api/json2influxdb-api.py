import sys
import argparse
import configparser
import json
import requests

# Helper method to print to stderr
def eprint(*args, **kwargs):
    # need to import sys first
    print(*args, file=sys.stderr, **kwargs)

def read_commandline_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            description='What the program does',
            epilog='Text at the bottom of help')
    parser.add_argument('-c', '--connection', action='store', nargs='?', required=True, 
                        help='name of the connection (section) in the config file to use for connecting to influxdb.')
    parser.add_argument('--config', action='store', nargs='?', 
                        help='the config file(path) to use.')
    
    return parser.parse_args()

def read_config(configfile) -> configparser.ConfigParser:
     config = configparser.ConfigParser()
     config.read_file(open(configfile))
     return config

def parse_json_input() -> str:
    # Read JSON input from stdin
    json_input = sys.stdin.read()

    # Parse JSON input
    try:
        data = json.loads(json_input)
        return data
    except json.JSONDecodeError as e:
        eprint("Error parsing JSON input:", e)
        return None

def get_influx_lineprotocol_string(parsed_data) -> str:
        # Measurements
        status_measurement = "meter-status"
        totals_measurement = "meter-totals"
        targets_measurement = "meter-targets"


        # Tags relevant for all data points/measurements
        general_tags = ""
        general_tags += ',id="{}"'.format(parsed_data.get("id").replace(" ","\\ "))
        general_tags += ',media="{}"'.format(parsed_data.get("media").replace(" ","\\ "))
        general_tags += ',meter="{}"'.format(parsed_data.get("meter").replace(" ","\\ "))
        general_tags += ',name="{}"'.format(parsed_data.get("name").replace(" ","\\ "))
        general_tags += ',ort="{}"'.format(parsed_data.get("ort").replace(" ","\\ "))
        general_tags += ',adresse="{}"'.format(parsed_data.get("adresse").replace(" ","\\ "))
        general_tags += ',whg="{}"'.format(parsed_data.get("whg").replace(" ","\\ "))
        general_tags += ',whg_lage="{}"'.format(parsed_data.get("whg_lage").replace(" ","\\ "))
        general_tags += ',zaehler_typ="{}"'.format(parsed_data.get("zaehler_typ").replace(" ","\\ "))
        general_tags += ',zaehler_typ_kurz="{}"'.format(parsed_data.get("zaehler_typ_kurz").replace(" ","\\ "))
        general_tags += ',zaehler_zusatz="{}"'.format(parsed_data.get("zaehler_zusatz").replace(" ","\\ "))
        general_tags += ',zaehler_seriennr_1="{}"'.format(parsed_data.get("zaehler_seriennr_1").replace(" ","\\ "))
        general_tags += ',zaehler_seriennr_2="{}"'.format(parsed_data.get("zaehler_seriennr_2").replace(" ","\\ "))
        general_tags += ',zaehler_seriennr_2_kurz="{}"'.format(parsed_data.get("zaehler_seriennr_2_kurz").replace(" ","\\ "))
        general_tags += ',lage_stockwerk="{}"'.format(parsed_data.get("lage_stockwerk").replace(" ","\\ "))
        general_tags += ',lage_raum="{}"'.format(parsed_data.get("lage_raum").replace(" ","\\ "))
        general_tags += ',lage_raum_kurz="{}"'.format(parsed_data.get("lage_raum_kurz").replace(" ","\\ "))
        general_tags += ',lage_raum_verortung="{}"'.format(parsed_data.get("lage_raum_verortung"))

        # output += ',device="{}"'.format(parsed_data.get("device").replace(" ","\\ "))             # example: "device": "rtlwmbus[00000001]"
        # output += ',rssi_dbm="{}"'.format(parsed_data.get("rssi_dbm").replace(" ","\\ "))         # example: "rssi_dbm": 137


        # Additional - measurememt specific - tags
        status_tags = ''
        totals_tags = ',total_date="{}"'.format(parsed_data.get("meter_date").replace(" ","\\ "))
        targets_tags = ',target_date="{}"'.format(parsed_data.get("target_date").replace(" ","\\ "))

        # Measurement specific fields
        status_fields = ' status="{}"'.format(parsed_data.get("status").replace(" ","\\ "))
        totals_fields = ' total_m3={}'.format(parsed_data.get("total_m3"))
        targets_fields = ' target_m3={}'.format(parsed_data.get("target_m3"))

        # Timestamp of meter
        # output += ',meter_timestamp="{}"'.format(parsed_data.get("timestamp").replace(" ","\\ "))


        # construct the data points
        output = ''
        # 1. data point - STATUS
        output += status_measurement + general_tags + status_tags + status_fields
        output += '\n'
         # 2. data point - TOTALS
        output += totals_measurement + general_tags + totals_tags + totals_fields
        output += '\n'
        # 3. data point - TARGETS
        output += targets_measurement + general_tags + targets_tags + targets_fields
        output += '\n'
        return output

def post_data(config, influx_string) -> None:
        # Post data
        protocol = 'http'
        if config.getboolean('ssl'):
            protocol += 's'
        
        host = config.get('host')
        port = config.getint('port')

        database = config.get('database')
        precision = config.get('precision')

        user =  config.get('user')
        password =  config.get('password')

        url = '{0}://{1}:{2}/write'.format(protocol, host, port)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'db': database,
            'precision': precision,
        }

        try:
            response = requests.post(
                url=url,
                params=params,
                headers=headers,
                data=influx_string,
                auth=(user, password),
            )
            print(response.status_code)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            eprint(error)

def main() -> None:
    
    args = read_commandline_args()
    configfile = args.config
    connection = args.connection

    config = read_config(configfile)

    if config.has_section(connection):
         config = config[connection]
    else:
        config = config['DEFAULT']
    

    # Parse JSON input
    parsed_data = parse_json_input()

    if parsed_data:
        influx_string = get_influx_lineprotocol_string(parsed_data)
        post_data(config, influx_string)

if __name__ == "__main__":
     main()