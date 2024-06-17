import re
import pandas as pd
from utils import clean_text_special_signs, contains_any, remove_trailing_characters

# used for user, weekday, month 
def process_column_contains_word(df, strings, threshold, new_column_name):
    """
    Rename the first column containing any of the strings provided in the list to a new column name.

    Args:
    - df: DataFrame, the input DataFrame.
    - strings: list of strings, the list of strings to search for in the DataFrame columns.
    - threshold: float, the threshold percentage of matching strings required to trigger the rename.
    - new_column_name: str, the new name to assign to the column.

    Returns:
    - df: DataFrame, the DataFrame with the renamed column if conditions are met.
    """
    candidate_columns = [col for col in df.columns[1:] if 'Col_' in col and 'Col_13' not in col]

    for column in candidate_columns:
        lowercase_values = df[column].apply(clean_text_special_signs)
        if lowercase_values.apply(lambda x: contains_any(x, strings)).mean() >= threshold:
            df = df.rename(columns={column: new_column_name})
            df[new_column_name] = df[new_column_name].apply(remove_trailing_characters)
            break
    return df

# used for user, weekday, month 
def process_column_contains_only_word(df, strings, threshold, new_column_name):
    """
    Rename the first column containing any of the strings provided in the list to a new column name.

    Args:
    - df: DataFrame, the input DataFrame.
    - strings: list of strings, the list of strings to search for in the DataFrame columns.
    - threshold: float, the threshold percentage of matching strings required to trigger the rename.
    - new_column_name: str, the new name to assign to the column.

    Returns:
    - df: DataFrame, the DataFrame with the renamed column if conditions are met.
    """
    candidate_columns = [col for col in df.columns if 'Col_' in col and 'Col_13' not in col]

    for column in candidate_columns:
        lowercase_values = df[column].apply(clean_text_special_signs)
        if lowercase_values.isin(strings).mean() >= threshold:
            df = df.rename(columns={column: new_column_name})
            df[new_column_name] = df[new_column_name].apply(remove_trailing_characters)
            break
    return df


def _match_special_pattern(text):
    """
    Check if the text matches the special pattern.
    """
    if text is None or text == "" or isinstance(text,float):
        return False
    pattern = re.compile(r'^(?=.*[A-Z].*[A-Z])(?=.*[0-9].*[0-9])[A-Z0-9]+([\-:][A-Z0-9]+)*$')
    return bool(pattern.match(text)) or text in ["UNKNOWN_LOCATION", "Null"]

def process_column_contains_pattern_word(df, strings, threshold, new_column_name):
    """
    Rename the first column containing any of the strings provided in the list to a new column name.

    Args:
    - df: DataFrame, the input DataFrame.
    - strings: list of strings, the list of strings to search for in the DataFrame columns.
    - threshold: float, the threshold percentage of matching strings required to trigger the rename.
    - new_column_name: str, the new name to assign to the column.

    Returns:
    - df: DataFrame, the DataFrame with the renamed column if conditions are met.
    """
    candidate_columns = [col for col in df.columns[1:] if 'Col_' in col and 'Col_13' not in col]

    for column in candidate_columns:
        lowercase_values = df[column].apply(clean_text_special_signs)
        match_ratio = lowercase_values.apply(lambda x: contains_any(x, strings)).sum() / len(lowercase_values)
        special_pattern_ratio = df[column].apply(_match_special_pattern).sum() / len(df[column])
        if match_ratio >= threshold or special_pattern_ratio >= threshold:
            df = df.rename(columns={column: new_column_name})
            break
    return df


def process_column_addr(df):
    """
    Finds columns in the DataFrame that contain values in square brackets
    with either a single hyphen or a mix of numbers, letters, hyphens, and spaces.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        list: A list of column names that match the criteria.
    """

    pattern = re.compile(r'\[\s*(?:-|\w[\w\s-]*)\s*\]')

    candidate_columns = [col for col in df.columns[1:] if 'Col_' in col and 'Col_13' not in col]

    for column in candidate_columns:
        if df[column].apply(lambda x: bool(pattern.match(str(x)))).sum() / len(df[column]) >= 0.8:
            df = df.rename(columns={column: 'addr'})
            break
    return df

def process_column_location(df):
    """
    Finds columns in the DataFrame with names starting with "Col_" and renames them to "location"
    if their values match those in the "user" column (with optional additional characters) at least 80% of the time.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with renamed columns.
    """

    if 'user' not in df.columns:
        return df

    def contains_user_value(user_value, cell_value):
        """
        Checks if the cell value contains the user value with optional additional characters like '/' and '@'.
        """
        if pd.isnull(cell_value) or pd.isnull(user_value):
            return False
        pattern =  r'[/@]*.*' + re.escape(user_value) 
        return bool(re.search(pattern, cell_value))


    candidate_columns = [col for col in df.columns[1:] if 'Col_' in col and 'Col_13' not in col]

    for column in candidate_columns:
        matching_rows = df.apply(lambda row: contains_user_value(row['user'], row[column]), axis=1)
        matching_percentage = matching_rows.mean()
        if matching_percentage >= 0.8:
            df = df.rename(columns={column: 'location'})
    
    return df

def merge_columns_to_content(df):
    """
    Merge all columns after the last non-"Col_" column into a single column named "Content".
    
    Args:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        pd.DataFrame: The modified DataFrame with a new "Content" column.
    """

    non_col_indices = [i for i, col in enumerate(df.columns) if "Col_" not in col]
    
    if not non_col_indices:
        raise ValueError("No column found that does not contain 'Col_' in its name.")
    
    last_non_col_index = non_col_indices[-1]

    if last_non_col_index >= 2:
        if "Col_" in df.columns[last_non_col_index - 1] and "Col_" in df.columns[last_non_col_index - 2]:
            last_non_col_index = non_col_indices[-2]
    
    columns_to_merge = df.columns[last_non_col_index + 1:]
    
    if columns_to_merge.empty:
        raise ValueError("No columns found to merge after the last non-'Col_' column.")
    
    df['Content'] = df[columns_to_merge].apply(lambda row: ' '.join([str(val) for val in row if val is not None]), axis=1).str.strip()
    

    df.drop(columns=columns_to_merge, inplace=True)
    
    return df
