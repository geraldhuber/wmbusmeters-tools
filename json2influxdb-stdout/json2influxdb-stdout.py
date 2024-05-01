import sys
sys.path.append('modules')
import cmd_args_helper
import c5isf
import minomess
import general

def output_data(influx_string: str) -> None:
    sys.stdout.write(influx_string)
    sys.stdout.write("\n")


def main() -> int:

    args = cmd_args_helper.readCommandlineArgs()

    # Parse JSON input
    for line in args.file:
        parsed_data = general.parseJsonInput(line)
        if parsed_data:
            match parsed_data.get("meter"):
                case "c5isf":
                    for influx_string in c5isf.getInfluxLineprotocol_c5isf(parsed_data):
                        output_data(influx_string)
                case "minomess":
                    influx_string = minomess.getInfluxLineprotocol_minomess(parsed_data)
                    output_data(influx_string)
    
    args.file.close()

    return sys.exit(cmd_args_helper.EXIT_SUCCESS)

if __name__ == "__main__":
    main()