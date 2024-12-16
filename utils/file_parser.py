from dataclasses import fields
from enum import Enum

from ..models.models import GeneticData, HeaderOrder


def get_header_order(line):
    assert line.startswith("#"), "Header line does not start with #"

    header_line_parts = line[1:].strip().split(",")
    assert len(header_line_parts) == len(
        HeaderOrder
    ), "The header line fields and required fields do not match"

    value_to_name = {member.value: member.name for member in HeaderOrder}

    return {
        value_to_name[field]: index for index, field in enumerate(header_line_parts)
    }


def convert_to_expected_types(data, data_class):
    converted_data = {}
    for field, value in data.items():
        try:
            field_type = next(f.type for f in fields(data_class) if f.name == field)
            if isinstance(value, field_type):
                converted_data[field] = value
            elif isinstance(field_type, type) and issubclass(field_type, Enum):
                converted_data[field] = field_type(value)
            else:
                converted_data[field] = field_type(value)
        except ValueError:
            print(
                f"The {field} is not a supported type of {field_type}. It's value is {value} whcih is not supported"
            )
    return converted_data


def parse_file_to_genetic_data(file_contents):
    header_order = get_header_order(file_contents[0])
    for line in file_contents[1:]:
        line_parts = line.strip().split(",")
        data = {field: line_parts[idx] for field, idx in header_order.items()}
        converted_data = convert_to_expected_types(data, GeneticData)
        genetic_data = GeneticData(**converted_data)
        yield genetic_data


def batch_insert_genetic_data_to_db(file_contents, individual_id, db_handler):
    genetic_data_list = list(parse_file_to_genetic_data(file_contents))
    db_handler.insert_genetic_data_to_db(genetic_data_list, individual_id)
