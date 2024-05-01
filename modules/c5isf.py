import general


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
        line += general.getGeneralTags(parsed_data)

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
        line += general.getGeneralTags(parsed_data)

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
        line += general.getGeneralTags(parsed_data)

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
        line += general.getGeneralTags(parsed_data)

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
        status = general.getStatusData(parsed_data)
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
