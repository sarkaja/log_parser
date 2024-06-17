import re
from date_time_processing import DateFinderPlural, apply_finder_method

def rename_first_column(df):
    """
    Renames the first column of the DataFrame based on specific conditions.

    Args:
        df (pd.DataFrame): The input DataFrame.
        date_finder_class (class): The class used to find date patterns (DateFinderNoSep).

    Returns:
        pd.DataFrame: The DataFrame with renamed first column.
    """
    first_column = df.columns[0]
    
    if first_column.startswith('Col_'):
        if df[first_column].astype(str).str.isdigit().all():
            df.rename(columns={first_column: 'logid'}, inplace=True)
        else:
            contains_words = any(df[first_column].apply(lambda x: bool(re.search(r'\w', str(x)))))
            if contains_words:
                lowercase_values = df[first_column].apply(lambda x: str(x).lower())
                pattern_found = any(lowercase_values.apply(lambda x: any(apply_finder_method(finder, x, DateFinderPlural) for finder in DateFinderPlural.finders)))

                if pattern_found:
                    df.rename(columns={first_column: 'logrecord'}, inplace=True)
                else:
                    only_special_chars_or_words = all(lowercase_values.apply(lambda x: bool(re.match(r'^[\w\s]+$', x)) or bool(re.match(r'^[\W_]+$', x))))
                    if only_special_chars_or_words:
                        df.rename(columns={first_column: 'Label'}, inplace=True)

            else:
                lowercase_values = df[first_column].apply(lambda x: str(x).lower())
                only_special_chars = all(lowercase_values.apply(lambda x: bool(re.match(r'^[\W_]+$', x))))
                if only_special_chars:
                    df.rename(columns={first_column: 'Label'}, inplace=True)
    
    return df
