import sys
import argparse
import json

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


# Helper method to print to stderr
def eprint(*args, **kwargs): # TODO: Add docstrings
    # need to import sys first
    print(*args, file=sys.stderr, **kwargs)

def read_commandline_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            description='What the program does',
            epilog='Text at the bottom of help')
    parser.add_argument(
        '-f', '--file',
        help='JSON input file. If \'-\' then stdin is used.',
        type=argparse.FileType('r'),
    )

    args = parser.parse_args()

    if args.file:
         input = args.file
    if not args.file:
        parser.print_usage()
        return sys.exit(EXIT_FAILURE)
    
    return args

def parse_json_input(json_line) -> dict[str, object]:
    # Parse JSON input
    try:
        data = json.loads(json_line)
        return data
    except json.JSONDecodeError as e:
        eprint("Error parsing JSON input:", e)
        return None

def getInfluxLineprotocol_minomess(parsed_data: dict[str, object]) -> str:
        # Measurements
        status_measurement = "meter-status"
        totals_measurement = "meter-totals"
        targets_measurement = "meter-targets"


        # Tags relevant for all data points/measurements
        general_tags = getGeneralTags(parsed_data)

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

def getStatusData(parsed_data: dict[str, object]) -> str:
    if parsed_data.get("status") != None:
        
        # Measurement
        line = "meter-status"

        # General tags
        line += getGeneralTags(parsed_data)

        # Specific tags
        # needs to start with a comma
        line += ''

        # Fields
        line += ' status="{}"'.format(parsed_data.get("status", "").replace(" ","\\ "))
    else:
        line = ""
    return line

def getCurrentValues_c5isf(parsed_data: dict[str, object]) -> str:

    total_energy_consumption_kwh = parsed_data.get("total_energy_consumption_kwh")
    total_volume_m3 = parsed_data.get("total_volume_m3")
    flow_temperature_c = parsed_data.get("flow_temperature_c")
    return_temperature_c = parsed_data.get("return_temperature_c")
    volume_flow_m3h = parsed_data.get("volume_flow_m3h")
    power_kw = parsed_data.get("power_kw")

    if (total_energy_consumption_kwh
        or total_volume_m3
        or flow_temperature_c
         or return_temperature_c
        or volume_flow_m3h
        or power_kw) > 0:

        # Measurement
        line = "meter-currentValues"

        # General tags
        line += getGeneralTags(parsed_data)

        # Specific tags
        # needs to start with a comma
        line += ''

        # Fields
        # Totals until now
        # The total heat energy consumption recorded by this meter.
        line += ' total_energy_consumption_kwh={}'.format(total_energy_consumption_kwh)

        # The total heating media volume recorded by this meter.
        line += ',total_volume_m3={}'.format(total_volume_m3)

        # Current values
        # Vorlauftemperatur
        line += ',flow_temperature_c={}'.format(flow_temperature_c)

        # Rücklauftemperatur
        line += ',return_temperature_c={}'.format(return_temperature_c)

        # The current heat media volume flow.
        line += ',volume_flow_m3h={}'.format(volume_flow_m3h)

        # The current power consumption.
        line += ',power_kw={}'.format(power_kw)
    else:
        line = ''

    return line

def getPreviousMonthsValues_c5isf(parsed_data: dict[str, object], month: int) -> str:
    previous_month_date = parsed_data.get("prev_"+str(month)+"_month", "").replace(" ","\\ ")
    if  len(previous_month_date) > 0:
        # Measurement
        line = "meter-previous_"+str(month)+"_MonthsValues"

        # General tags
        line += getGeneralTags(parsed_data)

        # Specific tags
        line += ',previous_month_date="{}"'.format(previous_month_date)

        # Fields
        line += ' previous_month_energy_kwh={}'.format(parsed_data.get("prev_"+str(month)+"_month_kwh", ""))
        line += ',previous_month_volume_m3={}'.format(parsed_data.get("prev_"+str(month)+"_month_m3", ""))
    else:
        line = ''

    return line

def getLastMonthsValues_c5isf(parsed_data: dict[str, object]) -> str:
    total_energy_consumption_last_month_kwh = parsed_data.get("total_energy_consumption_last_month_kwh", "")
    max_power_last_month_kw = parsed_data.get("max_power_last_month_kw", "")

    if (total_energy_consumption_last_month_kwh
        or  max_power_last_month_kw):

        # Measurement
        line = "meter-lastMonthsValues"

        # General tags
        line += getGeneralTags(parsed_data)

        # Specific tags
        line += '' # TODO: Calcualte date of last month.

        # Fields
        # Vormonats-Energie / The total heat energy consumption recorded at end of last month.
        line += ' total_energy_consumption_last_month_kwh={}'.format(total_energy_consumption_last_month_kwh)
        
        # Maximum power consumption last month.
        line += ',max_power_last_month_kw={}'.format(max_power_last_month_kw)
    else:
        line = ''

    return line

def getDueDateValues_c5isf(parsed_data: dict[str, object]) -> str:
    due_date = parsed_data.get("due_date", "").replace(" ","\\ ")

    if len(due_date) > 0:
        # Measurement
        line = "meter-dueDateValues"

        # General tags
        line += getGeneralTags(parsed_data)

        # Specific tags
        # Abrechnungstermin
        line += ',due_date="{}"'.format(due_date)

        # Fields
        # Energieverbrauch zum Abrechnungstermin
        line += ' energy_consumption_due_date_kwh={}'.format(parsed_data.get("due_energy_consumption_kwh", ""))
    else:
        line = ''

    return line

def getInfluxLineprotocol_c5isf(parsed_data: dict[str,object]) -> list[str]:
        output = []

        # Measurements
        status = getStatusData(parsed_data)
        if status != "":
            output.append(status)

        # Current Values
        currentValues = getCurrentValues_c5isf(parsed_data)
        if len(currentValues) > 0:
            output.append(currentValues)

        # Iterate through all previous month
        # meter provides max 1-14 month.
        for i in range(1,15):
            preMonthValues = getPreviousMonthsValues_c5isf(parsed_data, i)
            if len(preMonthValues) > 0:
                output.append(preMonthValues)
        
        # Values last month
        lastMonthsValues = getLastMonthsValues_c5isf(parsed_data)
        if len(lastMonthsValues) > 0:
            output.append(lastMonthsValues)

        # Due date values
        dueDateValues = getDueDateValues_c5isf(parsed_data)
        if len(dueDateValues) > 0:
            output.append(dueDateValues)

        return output


def getGeneralTags(parsed_data) -> str:
    ''' Generates a string that represents general tags as part of the influxdb lineprotocol

    Args:
        parsed_data (str): Input JSON data from wmbusmeters

    Returns:
        str:  Representation of general tags as part of the influxdb lineprotocol

    '''


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
    general_tags += ',lage_raum_verortung="{}"'.format(parsed_data.get("lage_raum_verortung").replace(" ","\\ "))
    # general_tags += ',device="{}"'.format(parsed_data.get("device").replace(" ","\\ "))             # example: "device": "rtlwmbus[00000001]"
    # general_tags += ',rssi_dbm="{}"'.format(parsed_data.get("rssi_dbm"))         # example: "rssi_dbm": 137
    
    return general_tags

def output_data(influx_string: str) -> None:
    sys.stdout.write(influx_string)
    sys.stdout.write("\n")


def main() -> int:

    args = read_commandline_args()

    # Parse JSON input
    for line in args.file:
        parsed_data = parse_json_input(line)
        if parsed_data:
            match parsed_data.get("meter"):
                case "c5isf":
                    for influx_string in getInfluxLineprotocol_c5isf(parsed_data):
                        output_data(influx_string)
                case "minomess":
                    influx_string = getInfluxLineprotocol_minomess(parsed_data)
                    output_data(influx_string)
    
    args.file.close()

    return sys.exit(EXIT_SUCCESS)

if __name__ == "__main__":
    main()