import json
import error_helper


def parseJsonInput(json_line) -> dict[str, object]:
    # Parse JSON input
    try:
        data = json.loads(json_line)
        return data
    except json.JSONDecodeError as e:
        error_helper.eprint("Error parsing JSON input:", e)
        return None

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
