import os
import json
import pandas as pd
from utils import load_json, drop_empty_columns

from process_columns import (
    process_column_contains_word,
    process_column_contains_pattern_word,
    process_column_contains_only_word,
    merge_columns_to_content,
    process_column_addr,
    process_column_location
)
from date_time_processing import process_time_date_columns, process_utc_timestamps, TimeFinderPlural, DateFinderPlural, find_and_process_day_column, find_and_process_year_column, process_time_date_no_sep_columns
from pid_tid_component_processing import (
    process_component_column_by_pattern,
    process_component_column_by_position,
    process_pid_column,
    process_pid_tid_columns,
    process_component_column_by_prefix
)
from process_first_column import rename_first_column

class LogParsingOrder:
    """
    A class used to structure logs in a DataFrame by applying a series of processing functions.

    Attributes:
        df (pd.DataFrame): The DataFrame containing log data.
        functions_needed (list): List of functions needed for further processing.
        flag (int): A flag to indicate the number of special conditions met during processing.

    Methods:
        load_json_values(path):
            Loads JSON data from the given file path.
        append_function(condition, func, kwargs=None):
            Appends a function to the functions_needed list if the condition is met.
        structure_logs():
            Processes the DataFrame by applying various log structuring functions.
    """

    def __init__(self, df):
        """
        Initializes LogStructurer with a DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame containing log data.
        """
        self.df = df
        self.functions_needed = []
        self.flag = 0

    def load_json_values(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, dict):
                values = list(data.values())
                if len(values) == 1 and isinstance(values[0], list):
                    return values[0]
                return values
            return data

    def append_function(self, condition, func, kwargs=None):
        """
        Appends a function to the functions_needed list if the condition is met.

        Args:
            condition (bool): The condition to check before appending the function.
            func (str): The function name to be appended.
            kwargs (dict, optional): The keyword arguments to pass to the function. Defaults to None.
        """
        if condition:
            if kwargs:
                self.functions_needed.append((func, kwargs))
            else:
                self.functions_needed.append(func)


    def structure_logs(self):
        """
        Processes the DataFrame by applying various log structuring functions.

        Returns:
            pd.DataFrame: The processed DataFrame.
            int: The flag indicating the number of special conditions met.
            list: The list of functions needed for further processing.
        """
        base_dir = os.path.dirname(os.path.dirname(__file__))
        
        json_paths = {
            'level': os.path.join(base_dir, 'data', 'level_values.json'),
            'month': os.path.join(base_dir, 'data', 'month_values.json'),
            'weekday': os.path.join(base_dir, 'data', 'weekday_values.json'),
            'program': os.path.join(base_dir, 'data', 'program_values.json'),
            'user': os.path.join(base_dir, 'data', 'user_values.json'),
            'node': os.path.join(base_dir, 'data', 'node_values.json'),
            'state': os.path.join(base_dir, 'data', 'state_values.json'),
            'flag': os.path.join(base_dir, 'data', 'flag_values.json'),
            'type': os.path.join(base_dir, 'data', 'type_values.json')
        }

        #values = {key: self.load_json_values(path) for key, path in json_paths.items()}

        values = {key: self.load_json_values(path) for key, path in json_paths.items()}

        self.df = process_column_contains_only_word(self.df, values['level'], threshold=0.8, new_column_name='level')

        self.df, flag_time1 = process_time_date_columns(self.df, column_type='time')
        self.append_function(flag_time1, 'process_time_date_columns', {'finder_class': TimeFinderPlural, 'column_type': 'time'})

        self.df = process_column_contains_only_word(self.df, values['month'], threshold=0.8, new_column_name='month')
        self.df = process_column_contains_only_word(self.df, values['weekday'], threshold=0.8, new_column_name='weekday')
        self.df = find_and_process_day_column(self.df)
        self.df = find_and_process_year_column(self.df)
        self.df = process_utc_timestamps(self.df)

        self.df, flag_date1 = process_time_date_columns(self.df, column_type='date')
        self.append_function(flag_date1, 'process_time_date_columns', {'finder_class': DateFinderPlural, 'column_type': 'date'})

        self.df = process_time_date_no_sep_columns(self.df)
        self.df = process_component_column_by_pattern(self.df)
        self.df = process_component_column_by_position(self.df, 'level')

        self.df, flag_pid = process_pid_column(self.df)
        self.append_function(flag_pid, process_component_column_by_pattern)
        self.append_function(flag_pid, process_pid_column)
        
        self.df = process_pid_tid_columns(self.df)
        self.df = process_column_contains_word(self.df, values['program'], threshold=0.8, new_column_name='program')
        self.df = process_column_contains_word(self.df, values['user'], threshold=0.4, new_column_name='user')
        self.df = process_column_contains_pattern_word(self.df, values['node'], threshold=0.4, new_column_name='node')
        self.df = process_column_contains_pattern_word(self.df, values['node'], threshold=0.4, new_column_name='node_repeat')
        self.df = process_component_column_by_prefix(self.df)
        self.df = process_column_contains_only_word(self.df, values['type'], threshold=0.4, new_column_name='type')
        self.df = process_column_contains_only_word(self.df, values['flag'], threshold=0.8, new_column_name='flag')
        self.df = process_column_contains_word(self.df, values['state'], threshold=0.5, new_column_name='state')
        self.df = process_component_column_by_position(self.df, 'state')
        
        self.df = rename_first_column(self.df)
        self.df = process_column_addr(self.df)
        self.df = process_column_location(self.df)
        
        self.df, flag_time2 = process_time_date_columns(self.df, column_type='time')
        self.append_function(flag_time2, 'process_time_date_columns', {'finder_class': TimeFinderPlural, 'column_type': 'time'})
        self.df, flag_date2 = process_time_date_columns(self.df, column_type='date')
        self.append_function(flag_date2, 'process_time_date_columns', {'finder_class': DateFinderPlural, 'column_type': 'date'})
        self.df = drop_empty_columns(self.df)
        self.df = merge_columns_to_content(self.df)
        flag = flag_date1+flag_date2+flag_pid+flag_time1+flag_time2
        return self.df, flag, self.functions_needed
