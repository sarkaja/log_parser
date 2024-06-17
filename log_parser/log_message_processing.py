import re
import os
import random
import pandas as pd
import chardet
from utils import clean_text_special_signs, load_json


base_dir = os.path.dirname(os.path.dirname(__file__))
months_path = os.path.join(base_dir, 'data', 'month_values.json')
weekdays_path = os.path.join(base_dir, 'data', 'weekday_values.json')

json_data_months = load_json(months_path)
months = json_data_months['month']
json_data_weekdays = load_json(weekdays_path)
weekdays = json_data_weekdays['weekday']

def detect_encoding(file_path):
    """
    Detect the encoding of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The detected encoding.
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']


#def load_and_split_messages(log_file_path):
#    """
#    Loads log messages from a file, shuffles them, and splits them into two parts.
#
#    Args:
#        log_file_path (str): The path to the log file.
#
#    Returns:
#        tuple: A tuple containing two lists:
#            - selected_messages (list of tuple): A list of tuples where each tuple contains an index and a log message from the selected subset (first 2000 messages).
#            - remaining_messages (list of tuple): A list of tuples where each tuple contains an index and a log message from the remaining messages.
#
#    The log messages are read from the file, shuffled randomly, and split into two parts:
#    the first part contains the first 2000 messages and the second part contains the remaining messages.
#    Each message is paired with its original index in the file.
#    """
#    found_encoding = detect_encoding(log_file_path)
#
#    with open(log_file_path, 'r', encoding=found_encoding) as file:
#        log_text = file.readlines()
#
#    total_messages = len(log_text)
#    indices = list(range(total_messages))
#    random.shuffle(indices)
#    
#    selected_indices = indices[:2000]
#    remaining_indices = indices[2000:]
#    
#    selected_messages = [(i, log_text[i]) for i in selected_indices]
#    remaining_messages = [(i, log_text[i]) for i in remaining_indices]
#
#    return selected_messages, remaining_messages
def load_and_split_messages(log_file_path):
    """
    Loads log messages from a file, shuffles them, and splits them into two parts if possible.

    Args:
    log_file_path (str): The path to the log file.

    Returns:
    tuple: A tuple containing two lists:
        - selected_messages (list of tuple): A list of tuples where each tuple contains an index and a log message from the selected subset (first 2000 messages).
        - remaining_messages (list of tuple): A list of tuples where each tuple contains an index and a log message from the remaining messages.

    The log messages are read from the file, shuffled randomly, and split into two parts if the total number of messages is at least 4000.
    Each message is paired with its original index in the file.
    """
    found_encoding = detect_encoding(log_file_path)

    with open(log_file_path, 'r', encoding=found_encoding) as file:
        log_text = file.readlines()

    total_messages = len(log_text)
    
    if total_messages < 4000:
        # If there are fewer than 4000 messages, do not split them
        selected_messages = [(i, log_text[i]) for i in range(total_messages)]
        remaining_messages = []
    else:
        indices = list(range(total_messages))
        random.shuffle(indices)
        
        selected_indices = indices[:2000]
        remaining_indices = indices[2000:]
        
        selected_messages = [(i, log_text[i]) for i in selected_indices]
        remaining_messages = [(i, log_text[i]) for i in remaining_indices]

    return selected_messages, remaining_messages

def determine_delimiter(log_messages):
    """
    Determine the delimiter used in the messages based on the presence of defined special characters.

    Args:
        log_messages (list): List of messages to analyze.

    Returns:
        str: The delimiter used in the messages, either '|' or ';', or None if no consistent delimiter is found.
    """

    pipe_count = 0
    semicolon_count = 0
    total_messages = len(log_messages)
    
    for log_message in log_messages:
        if log_message.count("|") >= 3:
            pipe_count += 1
        if log_message.count(";") >= 3:
            semicolon_count += 1
    
    if pipe_count / total_messages >= 0.8:
        return "|"
    elif semicolon_count / total_messages >= 0.8:
        return ";"
    
    return None


def split_message(log_message, delimiter):
    """
    Splits the message based on the given delimiter.

    Args:
        log_message (str): The input message.
        delimiter (str or None): The delimiter to split the message.

    Returns:
        list: List of parts split by the delimiter or by whitespace if no delimiter is defined.
    """
    if delimiter:
        return log_message.split(delimiter)
    return log_message.split()

def handle_combined_part(combined_part, bracket_count, part):
    """
    Handles the combined part inside brackets during message parsing.

    Args:
        combined_part (str): The combined part being constructed.
        bracket_count (int): Count of open brackets.
        part (str): The current part being processed.

    Returns:
        tuple: Combined part and updated bracket count.
    """
    combined_part += " " + part
    bracket_count -= 1
    if bracket_count == 0:
        return combined_part, bracket_count
    return None, bracket_count


def _process_combined_part(combined_part, values_to_columns_list):
    """
    Processing combined_part, which is the text of square brackets. 
    If there is any string inside that matches time or months or days of the week, combined_part will be split by delimiter. 
    Otherwise, the contents of the square brackets will be taken as a single value.

    Args:
        combined_part (str): The combined part to process.
        values_to_columns_list (list): The list to append the processed message_parts.
    """
    clean_combine = clean_text_special_signs(combined_part)

    # Looking for weekday or month match
    if any(re.search(rf'\b{day}\b', clean_combine) for day in weekdays) or any(re.search(rf'\b{month}\b', clean_combine) for month in months):
        values_to_columns_list.extend(combined_part.split())
    else:
        values_to_columns_list.append(combined_part)



def handle_parsed_parts(message_parts):
    """
    Handles the parsed parts from the split message, combining parts inside brackets and appending to parsed_parts.

    Args:
        parts (list): List of parts from split_message.

    Returns:
        list: Parsed parts after handling combined parts inside brackets.
    """

    values_to_columns_list = []
    combined_part = None
    bracket_count = 0


    for i, part in enumerate(message_parts):
        part = part.strip()
        if part.strip().startswith("*") and values_to_columns_list:
            values_to_columns_list[-1] += " " + part.strip()
        elif "[" in part and "]" not in part:
            if combined_part is None:
                combined_part = part
                bracket_count = 1
            else:
                combined_part += " " + part
                bracket_count += 1
        elif "]" in part and combined_part is not None:
            combined_part += " " + part
            bracket_count -= 1
            if bracket_count == 0:
                _process_combined_part(combined_part, values_to_columns_list)
                combined_part = None
        elif combined_part is not None:
            combined_part += " " + part
        else:
            values_to_columns_list.append(part)
    
    return values_to_columns_list


def process_data(messages, num_columns=13, delimiter=None):
    """
    Processes a list of messages into a DataFrame with a specified number of columns.

    Args:
        messages (list): List of message strings.
        num_columns (int): The number of columns to include in the output DataFrame.
        delimiter (str or None): The delimiter used to split the messages. If None, the delimiter is determined automatically.

    Returns:
        pd.DataFrame: Processed DataFrame with specified number of columns.
    """
    if delimiter is None:
        delimiter = determine_delimiter(messages)
    
    data = {f'Col_{i}': [None] * len(messages) for i in range(1, num_columns + 1)}
    
    for index, message in enumerate(messages):
        parts = split_message(message, delimiter)
        parsed_parts = handle_parsed_parts(parts)
        
        index_sloupce = 1
        for part in parsed_parts[:num_columns]: 
            data[f'Col_{index_sloupce}'][index] = part.strip()
            index_sloupce += 1

        if len(parsed_parts) > num_columns - 1:
            data[f'Col_{num_columns}'][index] = ' '.join(parsed_parts[num_columns - 1:]) 

    df = pd.DataFrame(data)
    df = df.dropna(axis=1, how='all')

    return df, delimiter


