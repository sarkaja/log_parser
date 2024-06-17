import pandas as pd
import re
from utils import clean_text_special_signs, remove_trailing_characters, drop_empty_columns

class DateFinderSingular:
    """
    A class for finding singular date patterns in a given text.

    Attributes:
        text (str): The input text to search for date patterns.

    Methods:
        find_dd_mm_yyyy_sep(): Finds dates in the format dd-mm-yyyy or dd/mm/yyyy or dd.mm.yyyy.
        find_mm_dd_yyyy_sep(): Finds dates in the format mm-dd-yyyy or mm/dd/yyyy or mm.mm.yyyy.
        find_yyyy_mm_dd_sep(): Finds dates in the format yyyy-mm-dd or yyyy/mm/dd or yyyy.mm.dd.
        find_yyyy_dd_mm_sep(): Finds dates in the format yyyy-dd-mm or yyyy/dd/mm or yyyy.dd.mm.
        find_dd_mm_sep(): Finds dates in the format dd-mm or dd/mm or dd.mm.
        find_mm_dd_sep(): Finds dates in the format mm-dd or mm/dd or mm.mm.
        find_dd_mm_yyyy_no_sep(): Finds dates in the format ddmmyyyy.
        find_mm_dd_yyyy_no_sep(): Finds dates in the format mmddyyyy.
        find_yyyy_mm_dd_no_sep(): Finds dates in the format yyyymmdd.
        find_yyyy_dd_mm_no_sep(): Finds dates in the format yyyyddmm.
        find_dd_mm_no_sep(): Finds dates in the format ddmm.
        find_mm_dd_no_sep(): Finds dates in the format mmdd.
        find_all_dates(): Finds and returns all matching date patterns in the text.
    """

    def __init__(self, text):
        self.text = text

    def find_dd_mm_yyyy_sep(self):
        """
        Finds dates in the format dd-mm-yyyy, dd/mm/yyyy, or dd.mm.yyyy.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^(?:0?[1-9]|[1-2]\d|3[0-1])([-/\.])(?:0?[1-9]|1[0-2])\1\d{4}$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_mm_dd_yyyy_sep(self):
        """
        Finds dates in the format mm-dd-yyyy, mm/dd/yyyy, or mm.mm.yyyy.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^(?:[0]?[1-9]|1[0-2])([-/\.])(?:[0]?[1-9]|[1-2]\d|3[0-1])\1\d{4}$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_yyyy_mm_dd_sep(self):
        """
        Finds dates in the format yyyy-mm-dd, yyyy/mm/dd, or yyyy.mm.dd.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^\d{4}([-/\.])(?:[0]?[1-9]|1[0-2])\1(?:[0]?[1-9]|[1-2]\d|3[0-1])$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_yyyy_dd_mm_sep(self):
        """
        Finds dates in the format yyyy-dd-mm, yyyy/dd/mm, or yyyy.dd.mm.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^\d{4}([-/\.])(?:0?[1-9]|[1-2]\d|3[0-1])\1(?:0?[1-9]|1[0-2])$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_dd_mm_sep(self):
        """
        Finds dates in the format dd-mm, dd/mm, or dd.mm.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'(?:[0]?[1-9]|[1-2]\d|3[0-1])(-|/|\.)(?:[0]?[1-9]|1[0-2])'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_mm_dd_sep(self):
        """
        Finds dates in the format mm-dd, mm/dd, or mm.mm.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'(?:[0]?[1-9]|1[0-2])(-|/|\.)(?:[0]?[1-9]|[1-2]\d|3[0-1])'
        return [match.group(0) for match in re.finditer(pattern, self.text)]


    def find_all_dates(self):
        """
        Finds and returns all matching date patterns in the text.

        Returns:
            list: A list of all matching date strings.
        """
        finders = [
            self.find_dd_mm_yyyy_sep,
            self.find_mm_dd_yyyy_sep,
            self.find_yyyy_mm_dd_sep,
            self.find_yyyy_dd_mm_sep,
            self.find_dd_mm_sep,
            self.find_mm_dd_sep
        ]

        for finder in finders:
            dates = finder()
            if dates:
                return dates
        return []

    finders = [
        'find_dd_mm_yyyy_sep',
        'find_mm_dd_yyyy_sep',
        'find_yyyy_mm_dd_sep',
        'find_yyyy_dd_mm_sep',
        'find_dd_mm_sep',
        'find_mm_dd_sep',
    ]

class DateFinderPlural:
    """
    A class for finding plural date patterns in a given text.

    Attributes:
        text (str): The input text to search for date patterns.

    Methods:
        find_dd_mm_yyyy_sep(): Finds dates in the format dd-mm-yyyy or dd/mm/yyyy or dd.mm.yyyy.
        find_mm_dd_yyyy_sep(): Finds dates in the format mm-dd-yyyy or mm/dd/yyyy or mm.mm.yyyy.
        find_yyyy_mm_dd_sep(): Finds dates in the format yyyy-mm-dd or yyyy/mm/dd or yyyy.mm.dd.
        find_yyyy_dd_mm_sep(): Finds dates in the format yyyy-dd-mm or yyyy/dd/mm or yyyy.dd.mm.
        find_dd_mm_sep(): Finds dates in the format dd-mm or dd/mm or dd.mm.
        find_mm_dd_sep(): Finds dates in the format mm-dd or mm/dd or mm.mm.
        find_dd_mm_yyyy_no_sep(): Finds dates in the format ddmmyyyy.
        find_mm_dd_yyyy_no_sep(): Finds dates in the format mmddyyyy.
        find_yyyy_mm_dd_no_sep(): Finds dates in the format yyyymmdd.
        find_yyyy_dd_mm_no_sep(): Finds dates in the format yyyyddmm.
        find_dd_mm_no_sep(): Finds dates in the format ddmm.
        find_mm_dd_no_sep(): Finds dates in the format mmdd.
        find_all_dates(): Finds and returns all matching date patterns in the text.
    """

    def __init__(self, text):
        self.text = text

    def find_dd_mm_yyyy_sep(self):
        """
        Finds dates in the format dd-mm-yyyy, dd/mm/yyyy, or dd.mm.yyyy.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'(?:0?[1-9]|[1-2]\d|3[0-1])([-/\.])(?:0?[1-9]|1[0-2])\1\d{4}'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_mm_dd_yyyy_sep(self):
        """
        Finds dates in the format mm-dd-yyyy, mm/dd/yyyy, or mm.mm.yyyy.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'(?:[0]?[1-9]|1[0-2])([-/\.])(?:[0]?[1-9]|[1-2]\d|3[0-1])\1\d{4}'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_yyyy_mm_dd_sep(self):
        """
        Finds dates in the format yyyy-mm-dd, yyyy/mm/dd, or yyyy.mm.dd.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'\d{4}([-/\.])(?:[0]?[1-9]|1[0-2])\1(?:[0]?[1-9]|[1-2]\d|3[0-1])'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_yyyy_dd_mm_sep(self):
        """
        Finds dates in the format yyyy-dd-mm, yyyy/dd/mm, or yyyy.dd.mm.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'\d{4}([-/\.])(?:0?[1-9]|[1-2]\d|3[0-1])\1(?:0?[1-9]|1[0-2])'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_dd_mm_sep(self):
        """
        Finds dates in the format dd-mm, dd/mm, or dd.mm.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'(?:[0]?[1-9]|[1-2]\d|3[0-1])(-|/|\.)(?:[0]?[1-9]|1[0-2])'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_mm_dd_sep(self):
        """
        Finds dates in the format mm-dd, mm/dd, or mm.mm.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'(?:[0]?[1-9]|1[0-2])(-|/|\.)(?:[0]?[1-9]|[1-2]\d|3[0-1])'
        return [match.group(0) for match in re.finditer(pattern, self.text)]


    def find_all_dates(self):
        """
        Finds and returns all matching date patterns in the text.

        Returns:
            list: A list of all matching date strings.
        """
        finders = [
            self.find_dd_mm_yyyy_sep,
            self.find_mm_dd_yyyy_sep,
            self.find_yyyy_mm_dd_sep,
            self.find_yyyy_dd_mm_sep,
            self.find_dd_mm_sep,
            self.find_mm_dd_sep,
        ]
        dates = []
        for finder in finders:
            dates.extend(finder())
        return dates

    finders = [
        'find_dd_mm_yyyy_sep',
        'find_mm_dd_yyyy_sep',
        'find_yyyy_mm_dd_sep',
        'find_yyyy_dd_mm_sep',
        'find_dd_mm_sep',
        'find_mm_dd_sep',
    ]


class DateFinderNoSep:
    """
    A class for finding singular date patterns in a given text.

    Attributes:
        text (str): The input text to search for date patterns.

    Methods:
        find_dd_mm_yyyy_no_sep(): Finds dates in the format ddmmyyyy.
        find_mm_dd_yyyy_no_sep(): Finds dates in the format mmddyyyy.
        find_yyyy_mm_dd_no_sep(): Finds dates in the format yyyymmdd.
        find_yyyy_dd_mm_no_sep(): Finds dates in the format yyyyddmm.
        find_dd_mm_no_sep(): Finds dates in the format ddmm.
        find_mm_dd_no_sep(): Finds dates in the format mmdd.
        find_all_dates(): Finds and returns all matching date patterns in the text.
    """

    def __init__(self, text):
        self.text = text


    def find_dd_mm_yyyy_no_sep(self):
        """
        Finds dates in the format ddmmyyyy.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^(?:0?[1-9]|[1-2]\d|3[0-1])(?:0?[1-9]|1[0-2])\d{4}$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_mm_dd_yyyy_no_sep(self):
        """
        Finds dates in the format mmddyyyy.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^(?:[0]?[1-9]|1[0-2])(?:[0]?[1-9]|[1-2]\d|3[0-1])\d{4}$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_yyyy_mm_dd_no_sep(self):
        """
        Finds dates in the format yyyymmdd.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^\d{4}(?:[0]?[1-9]|1[0-2])(?:[0]?[1-9]|[1-2]\d|3[0-1])$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_yyyy_dd_mm_no_sep(self):
        """
        Finds dates in the format yyyyddmm.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^\d{4}(?:0?[1-9]|[1-2]\d|3[0-1])(?:0?[1-9]|1[0-2])$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]


    def find_dd_mm_yy_no_sep(self):
        """
        Finds dates in the format ddmmyy.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^(?:0?[1-9]|[1-2]\d|3[0-1])(?:0?[1-9]|1[0-2])\d{2}$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_mm_dd_yy_no_sep(self):
        """
        Finds dates in the format mmddyy.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^(?:[0]?[1-9]|1[0-2])(?:[0]?[1-9]|[1-2]\d|3[0-1])\d{2}$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]
    
    def find_yy_dd_mm_no_sep(self):
        """
        Finds dates in the format yyddmm.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^\d{2}(?:0?[1-9]|[1-2]\d|3[0-1])(?:0?[1-9]|1[0-2])$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_yy_mm_dd_no_sep(self):
        """
        Finds dates in the format yymmdd.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^\d{2}(?:[0]?[1-9]|1[0-2])(?:[0]?[1-9]|[1-2]\d|3[0-1])$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_dd_mm_no_sep(self):
        """
        Finds dates in the format ddmm.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^(?:[0]?[1-9]|[1-2]\d|3[0-1])(?:[0]?[1-9]|1[0-2])$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_mm_dd_no_sep(self):
        """
        Finds dates in the format mmdd.

        Returns:
            list: A list of matching date strings.
        """
        pattern = r'^(?:[0]?[1-9]|1[0-2])(?:[0]?[1-9]|[1-2]\d|3[0-1])$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]


    finders = [
        'find_dd_mm_yyyy_no_sep',
        'find_mm_dd_yyyy_no_sep',
        'find_yyyy_mm_dd_no_sep',
        'find_yyyy_dd_mm_no_sep',
        'find_dd_mm_yy_no_sep',
        'find_mm_dd_yy_no_sep',
        'find_yy_dd_mm_no_sep',
        'find_yy_mm_dd_no_sep',
        'find_dd_mm_no_sep',
        'find_mm_dd_no_sep',
    ]



class TimeFinderSingular:
    """
    A class to find singular time formats in a given text.

    Attributes:
        text (str): The input text to search for time formats.

    Methods:
        find_24h_format_with_milliseconds(): Finds 24-hour format times with milliseconds.
        find_24h_format_with_seconds(): Finds 24-hour format times with seconds.
        find_24h_format_without_seconds(): Finds 24-hour format times without seconds.
        find_all_times(): Finds all times using various formats.
    """
    def __init__(self, text):
        """
        Initializes the TimeFinder_singular with the provided text.

        Args:
            text (str): The input text to search for time formats.
        """
        self.text = text

    def find_24h_format_with_milliseconds(self):
        """
        Finds 24-hour format times with milliseconds in the text.

        Returns:
            list: A list of matching time strings.
        """
        pattern = r'^(?:[01]\d|\d|2[0-3])([:\.])(?:[0-5]\d|\d)\1(?:[0-5]\d|\d)(?:(:|\.|,)\d{1,6})$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_24h_format_with_seconds(self):
        """
        Finds 24-hour format times with seconds in the text.

        Returns:
            list: A list of matching time strings.
        """
        pattern = r'^(?:[01]\d|\d|2[0-3])([:\.])(?:[0-5]\d|\d)\1(?:[0-5]\d|\d)$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_24h_format_without_seconds(self):
        """
        Finds 24-hour format times without seconds in the text.

        Returns:
            list: A list of matching time strings.
        """
        pattern = r'^(?:[01]\d|\d|2[0-3])([:\.])(?:[0-5]\d|\d)$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    finders = [
        'find_24h_format_with_milliseconds',
        'find_24h_format_with_seconds',
        'find_24h_format_without_seconds',
    ]

class TimeFinderPlural:
    """
    A class to find plural time formats in a given text.

    Attributes:
        text (str): The input text to search for time formats.

    Methods:
        find_24h_format_with_milliseconds(): Finds 24-hour format times with milliseconds.
        find_24h_format_with_seconds(): Finds 24-hour format times with seconds.
        find_24h_format_without_seconds(): Finds 24-hour format times without seconds.
        find_all_times(): Finds all times using various formats.
    """
    def __init__(self, text):
        """
        Initializes the TimeFinder_plural with the provided text.

        Args:
            text (str): The input text to search for time formats.
        """
        self.text = text

    def find_24h_format_with_milliseconds(self):
        """
        Finds 24-hour format times with milliseconds in the text.

        Returns:
            list: A list of matching time strings.
        """
        pattern = r'\b(?:[01]?\d|2[0-3])([:\.])(?:[0-5]?\d)\1(?:[0-5]?\d)(?:(:|\.|,)\d{1,6})\b'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_24h_format_with_seconds(self):
        """
        Finds 24-hour format times with seconds in the text.

        Returns:
            list: A list of matching time strings.
        """
        pattern = r'\b(?:[01]?\d|2[0-3])([:\.])(?:[0-5]?\d)\1(?:[0-5]?\d)\b'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_24h_format_without_seconds(self):
        """
        Finds 24-hour format times without seconds in the text.

        Returns:
            list: A list of matching time strings.
        """
        pattern = r'\b(?:[01]?\d|2[0-3])([:\.])(?:[0-5]?\d)\b'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    finders = [
        'find_24h_format_with_milliseconds',
        'find_24h_format_with_seconds',
        'find_24h_format_without_seconds',
    ]


class TimeFinderNoSep:
    """
    A class to find singular time formats in a given text.

    Attributes:
        text (str): The input text to search for time formats.

    Methods:
        find_24h_format_with_milliseconds(): Finds 24-hour format times with milliseconds.
        find_24h_format_with_seconds(): Finds 24-hour format times with seconds.
        find_24h_format_without_seconds(): Finds 24-hour format times without seconds.
        find_all_times(): Finds all times using various formats.
    """
    def __init__(self, text):
        """
        Initializes the TimeFinder_singular with the provided text.

        Args:
            text (str): The input text to search for time formats.
        """
        self.text = text

    def find_24h_format_with_milliseconds_no_sep(self):
        """
        Finds 24-hour format times with milliseconds in the text.

        Returns:
            list: A list of matching time strings.
        """
        pattern = r'^(?:[01]\d|\d|2[0-3])(?:[0-5]\d|\d)(?:[0-5]\d|\d)(?:\d{1,6})$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_24h_format_with_seconds_no_sep(self):
        """
        Finds 24-hour format times with seconds in the text.

        Returns:
            list: A list of matching time strings.
        """
        pattern = r'^(?:[01]\d|\d|2[0-3])(?:[0-5]\d|\d)(?:[0-5]\d|\d)$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    def find_24h_format_without_seconds_no_sep(self):
        """
        Finds 24-hour format times without seconds in the text.

        Returns:
            list: A list of matching time strings.
        """
        pattern = r'^(?:[01]\d|\d|2[0-3])(?:[0-5]\d|\d)$'
        return [match.group(0) for match in re.finditer(pattern, self.text)]

    finders = [
        'find_24h_format_with_milliseconds_no_sep',
        'find_24h_format_with_seconds_no_sep',
        'find_24h_format_without_seconds_no_sep',
    ]




def process_time_date_columns(df, finder_class=None, column_type='time'):
    """
    Finds columns in the DataFrame that contain specific patterns (date or time) and processes them.

    Args:
        df (pd.DataFrame): The input DataFrame.
        finder_class (class, optional): The class used to find patterns. Defaults to None.
        column_type (str, optional): The type of column to process ('date' or 'time'). Defaults to 'date'.

    Returns:
        pd.DataFrame: The processed DataFrame with identified columns cleaned and renamed.
    """
    def identify_column(df, finder_class):
        """
        Identifies columns in the DataFrame that contain specific patterns based on the given finder class.

        Args:
            df (pd.DataFrame): The input DataFrame.
            finder_class (class): The class used to find patterns.

        Returns:
            tuple: A tuple containing the identified column name and the finder method name.
                   Returns (None, None) if no column is found.
        """
        for finder in finder_class.finders:
            for column in df.columns:
                if 'Col_' in column:
                    lowercase_values = df[column].apply(clean_text_special_signs)
                    pattern = lowercase_values.apply(lambda x: bool(apply_finder_method(finder, x, finder_class)))
                    if pattern.mean() >= 0.8:
                        return column, finder
        return None, None

    def clean_and_rename_column(df, column, finder, finder_class, column_type):
        """
        Cleans and renames the identified column.

        Args:
            df (pd.DataFrame): The input DataFrame.
            column (str): The name of the column to clean and rename.
            finder (str): The finder method name.
            finder_class (class): The class used to find patterns.
            column_type (str): The type of column to rename ('date' or 'time').

        Returns:
            pd.DataFrame: The DataFrame with the cleaned and renamed column.
        """
        df[column] = df[column].apply(remove_trailing_characters)
        df = df.rename(columns={column: column_type})
        return df

    def process_mixed_column(df, column, finder, finder_class, column_type):
        """
        Processes a column with mixed values, moving specific pattern values to a new column.

        Args:
            df (pd.DataFrame): The input DataFrame.
            column (str): The name of the column to process.
            finder (str): The finder method name.
            finder_class (class): The class used to find patterns.
            column_type (str): The type of column to create ('date' or 'time').

        Returns:
            pd.DataFrame: The DataFrame with the processed mixed values column.
        """
        original_column_index = df.columns.get_loc(column)
        df.insert(original_column_index + 1, column_type, '')

        lowercase_values = df[column].apply(clean_text_special_signs)
        df[column_type] = lowercase_values.apply(
            lambda x: next(iter(apply_finder_method(finder, x, finder_class)), '') if apply_finder_method(finder, x, finder_class) else x
        )

        df[column] = df.apply(
            lambda row: row[column].replace(row[column_type], '') if row[column_type] != '' else row[column], axis=1
        )
        df[column] = df[column].apply(remove_trailing_characters)
        return df

    flag = 0
    column_type_plural = column_type.capitalize() + "FinderPlural"
    column_type_singular = column_type.capitalize() + "FinderSingular"

    if finder_class == globals()[column_type_plural]:
        column, finder = identify_column(df, globals()[column_type_plural])
        if column:
            df = process_mixed_column(df, column, finder, globals()[column_type_plural], column_type)
            flag = 1

    column, finder = identify_column(df, globals()[column_type_singular])
    if column:
        df = clean_and_rename_column(df, column, finder, globals()[column_type_singular], column_type)
    else:
        column, finder = identify_column(df, globals()[column_type_plural])
        if column:
            df = process_mixed_column(df, column, finder, globals()[column_type_plural], column_type)
            flag = 1

    return df, flag


def apply_finder_method(method_name, text, FinderClass):
    """
    Applies a specified method of the FinderClass to find time patterns in the text.

    Args:
        method_name (str): The name of the method to apply.
        text (str): The text to search for time patterns.
        FinderClass (class): The class containing the method.

    Returns:
        list: A list of matching time strings.
    """
    finder = FinderClass(text)
    return getattr(finder, method_name)()


def _process_day_column(df, candidate_col, target_col):
    """
    Process a column as 'day' if it contains valid day values.

    This function checks if the specified candidate column in the DataFrame contains valid day values 
    (from 1 to 31). If at least 90% of the values match the day pattern, the column is renamed to 'day' 
    and any trailing characters are removed. Non-matching values are moved to a 'rest_day' column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column to be processed.
    candidate_col (str): The name of the candidate column to be checked and processed.
    target_col (str): The name of the target column where the processed day values will be stored.

    Returns:
    tuple: A tuple containing the modified DataFrame and a boolean indicating if the column was processed.
    """
    lowercase_values = df[candidate_col].apply(clean_text_special_signs)
    valid_day_mask = lowercase_values.str.match(r'^(0?[1-9]|[12][0-9]|3[01])$')
    if valid_day_mask.mean() >= 0.9:
        df[target_col] = df[candidate_col]
        df = df.rename(columns={candidate_col: 'day'})
        df['day'] = df['day'].apply(remove_trailing_characters)
        return df, True
    return df, False

def find_and_process_day_column(df):
    """
    Find and process a day column based on adjacent columns.

    This function attempts to identify a column containing day values by checking the columns adjacent to 
    key columns ('month' and 'weekday'). If a valid day column is found, it processes the column using 
    the `process_day_column` function.

    Parameters:
    df (pd.DataFrame): The DataFrame in which to find and process the day column.

    Returns:
    pd.DataFrame: The modified DataFrame with the processed day column.
    """
    key_columns = ['month', 'weekday']
    for key_col in key_columns:
        key_idx = df.columns.get_loc(key_col) if key_col in df.columns else -1
        candidate_columns = []
        if key_idx > 0:
            prev_col = df.columns[key_idx - 1]
            if prev_col.startswith('Col_') and prev_col != 'Col_13':
                candidate_columns.append(prev_col)
        if key_idx < len(df.columns) - 1:
            next_col = df.columns[key_idx + 1]
            if next_col.startswith('Col_') and next_col != 'Col_13':
                candidate_columns.append(next_col)
        for col in candidate_columns:
            df, found = _process_day_column(df, col, col)
            if found:
                return df
    return df

def _process_year_column(df, candidate_col, target_col):
    """
    Process a column as 'year' if it contains valid year values.

    This function checks if the specified candidate column in the DataFrame contains valid year values 
    (from 1900 to 3000). If at least 90% of the values match the year pattern, the column is renamed to 'year' 
    and any trailing characters are removed. Non-matching values are moved to a 'rest_year' column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column to be processed.
    candidate_col (str): The name of the candidate column to be checked and processed.
    target_col (str): The name of the target column where the processed year values will be stored.

    Returns:
    tuple: A tuple containing the modified DataFrame and a boolean indicating if the column was processed.
    """
    lowercase_values = df[candidate_col].apply(clean_text_special_signs)
    valid_year_mask = lowercase_values.str.match(r'^(19[0-9]{2}|2[0-9]{3}|3000)$')
    if valid_year_mask.mean() >= 0.9:
        df[target_col] = df[candidate_col]
        df = df.rename(columns={candidate_col: 'year'})
        df['year'] = df['year'].apply(remove_trailing_characters)

        return df, True
    return df, False

def find_and_process_year_column(df):
    """
    Find and process a year column based on adjacent columns.

    This function attempts to identify a column containing year values by checking the columns adjacent to 
    key columns ('month', 'weekday', and 'time'). If a valid year column is found, it processes the column using 
    the `process_year_column` function.

    Parameters:
    df (pd.DataFrame): The DataFrame in which to find and process the year column.

    Returns:
    pd.DataFrame: The modified DataFrame with the processed year column.
    """
    key_columns = ['month', 'weekday', 'time']
    for key_col in key_columns:
        key_idx = df.columns.get_loc(key_col) if key_col in df.columns else -1
        candidate_columns = []
        if key_idx > 0:
            prev_col = df.columns[key_idx - 1]
            if prev_col.startswith('Col_') and prev_col != 'Col_13':
                candidate_columns.append(prev_col)
        if key_idx < len(df.columns) - 1:
            next_col = df.columns[key_idx + 1]
            if next_col.startswith('Col_') and next_col != 'Col_13':
                candidate_columns.append(next_col)
        for col in candidate_columns:
            df, found = _process_year_column(df, col, col)
            if found:
                return df
    return df


def process_utc_timestamps(df):
    """Detect and convert columns with UTC timestamps."""
    for column in df.columns:
        if column.startswith("Col_"):
            numeric_values = pd.to_numeric(df[column], errors='coerce')
            if numeric_values.count() / len(df) >= 0.9:
                converted_times = pd.DataFrame()
                converted_times['timestamp'] = pd.to_datetime(numeric_values, unit='s', utc=True).dt.strftime('%Y-%m-%d')
                converted_times['timestamp'] = pd.to_datetime(converted_times['timestamp'])
                if (converted_times['timestamp'] >= pd.Timestamp('1990-01-01')).all():
                    df.rename(columns={column: "timestamp"}, inplace=True)
                    break
                else:
                    pass
    return df



def identify_columns_date_time_no_sep(df, finder_class):
    """
    Identifies columns in the DataFrame that contain values based on the given finder class.

    Args:
        df (pd.DataFrame): The input DataFrame.
        finder_class (class): The class used to find patterns.

    Returns:
        list: A list of identified column names.
    """
    identified_columns = []
    seen_columns = set()
    
    for finder in finder_class.finders:
        for column in df.columns:
            if 'Col_' in column and column not in seen_columns:
                lowercase_values = df[column].apply(clean_text_special_signs)
                pattern = lowercase_values.apply(lambda x: bool(apply_finder_method(finder, x, finder_class)))
                if pattern.mean() >= 0.8:
                    lengths = lowercase_values.apply(len)
                    length_counts = lengths.value_counts()
                    if not length_counts.empty:
                        most_common_length = length_counts.index[0]
                        valid_lengths = [most_common_length]
                        if len(length_counts) > 1:
                            most_common_length2 = length_counts.index[1]
                            valid_lengths.append(most_common_length2)
                        length_consistency = lengths.isin(valid_lengths).mean()
                        if length_consistency >= 0.9:
                            identified_columns.append(column)
                            seen_columns.add(column)
                    
    return identified_columns

def process_time_date_no_sep_columns(df):
    """
    Renames columns in the DataFrame based on date and time patterns.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with renamed columns if applicable.
    """
    if not any(col in df.columns for col in ["time", "date", "year", "day"]):
        date_columns = identify_columns_date_time_no_sep(df, DateFinderNoSep)
        time_columns = identify_columns_date_time_no_sep(df, TimeFinderNoSep)

        date_column_set = set(date_columns)
        time_column_set = set(time_columns)

        common_columns = date_column_set & time_column_set

        if len(common_columns) >= 2:
            unique_count_1 = df[common_columns[0]].nunique()
            unique_count_2 = df[common_columns[1]].nunique()

            if unique_count_1 <= unique_count_2:
                df.rename(columns={common_columns[0]: "date", common_columns[1]: "time"}, inplace=True)
            else:
                df.rename(columns={common_columns[0]: "time", common_columns[1]: "date"}, inplace=True)
        elif len(common_columns) == 1:
            common_column = list(common_columns)[0]
            df.rename(columns={common_column: "date"}, inplace=True)

            other_date_columns = list(date_column_set - common_columns)
            other_time_columns = list(time_column_set - common_columns)

            if other_date_columns:
                df.rename(columns={other_date_columns[0]: "time"}, inplace=True)
            elif other_time_columns:
                df.rename(columns={other_time_columns[0]: "time"}, inplace=True)
        else:
            if date_columns and time_columns:
                unique_count_date = df[date_columns[0]].nunique()
                unique_count_time = df[time_columns[0]].nunique()

                if unique_count_date <= unique_count_time:
                    df.rename(columns={date_columns[0]: "date", time_columns[0]: "time"}, inplace=True)
                else:
                    df.rename(columns={time_columns[0]: "time", date_columns[0]: "date"}, inplace=True)
            elif date_columns:
                df.rename(columns={date_columns[0]: "date"}, inplace=True)
            elif time_columns:
                df.rename(columns={time_columns[0]: "time"}, inplace=True)
    return df