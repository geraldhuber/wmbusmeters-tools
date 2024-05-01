
import general

def getInfluxLineprotocol_minomess(parsed_data: dict[str, object]) -> str:
        # Measurements
        status_measurement = "meter-status"
        totals_measurement = "meter-totals"
        targets_measurement = "meter-targets"


        # Tags relevant for all data points/measurements
        general_tags = general.getGeneralTags(parsed_data)

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
