import re
import pandas as pd
from collections import Counter
from utils import lower_strip_text, matches_pattern, is_only_numeric, is_only_special, remove_numbers_and_brackets
import warnings

def process_component_column_by_pattern(df):
    """
    Rename a column to 'component' based on specific patterns.

    This function scans the columns of the DataFrame starting from the second column,
    looking for columns that meet specific criteria based on a regular expression pattern.
    If a column has a high proportion of values matching the pattern, it is renamed to 'component'.

    Args:
        df (pd.DataFrame): The input DataFrame to process.

    Returns:
        pd.DataFrame: The DataFrame with the column renamed to 'component', if a matching column is found.
    """
    candidate_columns = [col for col in df.columns[1:] if 'Col_' in col and 'Col_13' not in col] 
    pattern_component = r'(?<=[a-zA-Z\-:_\)\]\}][@\[:])\d+(?=(\]:|\:\]|\:$|\]$|$))|.+:$'
    for column in candidate_columns:
        lowercase_values = df[column].apply(lower_strip_text)
        matching_pattern_sum = lowercase_values.apply(lambda x: matches_pattern(x, pattern_component)).sum()
        if matching_pattern_sum / len(lowercase_values) >= 0.8:
            df = df.rename(columns={column: 'component'})
            break
    return df


def process_component_column_by_position(df, specified_column):
    """
    Rename a column to 'component' based on its position relative to a specified column.

    This function checks if the specified column exists in the DataFrame and 'component' is not already a column.
    It then looks for adjacent columns (either immediately before or after the specified column) that meet specific
    criteria (not being only numeric or special characters) and renames such a column to 'component'.

    Args:
        df (pd.DataFrame): The input DataFrame to process.
        specified_column (str): The name of the column to use as a reference point for renaming.

    Returns:
        pd.DataFrame: The DataFrame with the column renamed to 'component', if a matching column is found.
    """
    if 'component' not in df.columns and specified_column in df.columns:
        candidate_columns = [col for col in df.columns[1:] if 'Col_' in col and 'Col_13' not in col]
        info_index = df.columns.get_loc(specified_column)
        for col in candidate_columns:
            if df.columns.get_loc(col) == info_index - 1 or df.columns.get_loc(col) == info_index + 1:
                if not df[col].apply(lambda x: is_only_numeric(x) or is_only_special(x)).any():
                    df = df.rename(columns={col: 'component'})
                    break
    return df


def process_component_column_by_prefix(df):
    """
    Find and rename a column to 'component' based on specific criteria.
    
    Args:
        df (pd.DataFrame): The DataFrame to process.
    
    Returns:
        pd.DataFrame: The DataFrame with a renamed component column if criteria are met.
    """
    if 'component' in df.columns:
        return df

    candidate_columns = [col for col in df.columns[1:] if 'Col_' in col and 'Col_13' not in col]
    
    for column in candidate_columns:
        separator = determine_separator_in_column(df[column])
        if separator:
            prefixes = df[column].dropna().apply(lambda x: extract_prefix(x, separator))
            non_numeric_prefixes = [prefix for prefix in prefixes if prefix and not prefix.isdigit()]
            prefix_counts = Counter(non_numeric_prefixes)
            common_prefixes = [prefix for prefix, count in prefix_counts.items() if count / len(df) >= 0.08]

            if len(common_prefixes) <= 10 and sum(prefix_counts[prefix] for prefix in common_prefixes) / len(df) >= 0.8:
                df = df.rename(columns={column: 'component'})
                break

    return df

def determine_separator_in_column(column):
    """
    Determine the most common separator in a column.
    
    Args:
        column (pd.Series): The column to analyze.
    
    Returns:
        str: The most common separator ('_', '.', or 'upper').
    """
    separators = {'_': 0, '.': 0, 'upper': 0}
    
    for value in column.dropna():
        if '_' in value:
            separators['_'] += 1
        elif '.' in value:
            separators['.'] += 1
        elif re.match(r'[A-Z].*[A-Z]', value):
            separators['upper'] += 1
    
    most_common_separator = max(separators, key=separators.get)
    return most_common_separator if separators[most_common_separator] > 0 else None

def extract_prefix(value, separator):
    """
    Extract the prefix from the value based on a specific separator.
    
    Args:
        value (str): The value from which to extract the prefix.
        separator (str): The separator to use for extracting the prefix.
    
    Returns:
        str: The extracted prefix or None if no prefix is found.
    """
    if separator == '_':
        return value.split('_')[0]
    elif separator == '.':
        return value.split('.')[0]
    elif separator == 'upper':
        match = re.match(r'^([A-Z][a-z]*)(?=[A-Z])', value)
        if match:
            return match.group(1)
    return None


def _extract_pid(text):
    """
    Extracts the pid from the given text based on a pattern.
    
    Args:
        text (str): The input text from which pid needs to be extracted.
        
    Returns:
        str: The extracted pid or None if no pattern is matched.
    """
    pattern = r'(?P<pid>\d+)'
    matches = re.findall(pattern, text)
    return matches[-1] if matches else ''

def process_pid_column(df):
    """
    Process the 'pid' in the DataFrame based on a pattern.
    
    This function identifies and extracts 'pid' values from the 'component' column if the column exists 
    and the majority of the rows contain 'pid' patterns. If the 'component' column does not exist, 
    it searches for 'pid' patterns in columns with names starting with 'Col_' (except 'Col_13').
    It also removes these patterns from the original columns after extraction.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        pd.DataFrame: The modified DataFrame with a new 'pid' column if applicable.
    """
    PATTERN_PID = r'(?<=[a-zA-Z0-9\-:_\)\]\}][@\[:])\d+(?=(\]:|\:\]|\:$|\]$|$))'
    flag = 0
    if 'component' in df.columns:
        total_rows = len(df)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            rows_with_pid = df['component'].str.contains(PATTERN_PID, na=False).sum()

        if rows_with_pid / total_rows >= 0.1:
            df['pid'] = df['component'].apply(lambda x: _extract_pid(x) if x is not None and re.search(PATTERN_PID, x) else '')
            df['component'] = df['component'].str.replace(PATTERN_PID, '', regex=True).str.strip()
            idx = df.columns.get_loc('component') + 1
            df.insert(idx, 'pid', df.pop('pid'))
            df['component'] = df['component'].apply(remove_numbers_and_brackets)
            df['pid'] = df['pid'].apply(remove_numbers_and_brackets)
            flag = 1
    #else:
    #    candidate_columns = [col for col in df.columns[1:] if 'Col_' in col and 'Col_13' not in col]
    #    for col in candidate_columns:
    #        total_rows = len(df)
    #        rows_with_pid = df[col].str.contains(PATTERN_PID, na=False).sum()
    #        
    #        if rows_with_pid / total_rows >= 0.5:
    #            df[f'pid_{col}'] = df[col].apply(lambda x: _extract_pid(x) if x is not None and re.search(PATTERN_PID, x) else None)
    #            df[col] = df[col].str.replace(PATTERN_PID, '', regex=True).str.strip()
    #            idx = df.columns.get_loc(col) + 1
    #            df.insert(idx, f'pid_{col}', df.pop(f'pid_{col}'))
    #            df[col] = df[col].apply(remove_numbers_and_brackets)
    #            df[f'pid_{col}'] = df[f'pid_{col}'].apply(remove_numbers_and_brackets)
    #            flag = 1
#
    return df, flag



def process_pid_tid_columns(df):
    """
    Rename columns to 'pid' and 'tid' based on specific criteria.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The DataFrame with renamed columns.
    """
    if 'pid' in df.columns or 'tid' in df.columns:
        return df
    
    candidate_columns = [col for col in df.columns[1:] if 'Col_' in col and 'Col_13' not in col]
    numerical_columns = []
    
    for column in candidate_columns:
        if df[column].apply(lambda x: pd.to_numeric(x, errors='coerce')).notna().sum() / len(df) >= 0.8:
            if df[column].apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna().astype(int).ge(10).all():
                numerical_columns.append(column)

    if len(numerical_columns) == 1:
        df = df.rename(columns={numerical_columns[0]: 'pid'})
    elif ('date' in df.columns and 'time' in df.columns) or ('day' in df.columns and 'time' in df.columns):
        for i, column in enumerate(numerical_columns):
            if 'Col_' in column:
                if i == 0:
                    df = df.rename(columns={column: 'pid'})
                elif i == 1:
                    df = df.rename(columns={column: 'tid'})
                if i >= 1:
                    break
    else:
        for i, column in enumerate(numerical_columns):
            if i == 0:
                df = df.rename(columns={column: 'pid'})
            elif i == 1:
                df = df.rename(columns={column: 'tid'})
            if i >= 1:
                break

    return df