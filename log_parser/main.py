import pandas as pd
from log_parsing_order import LogParsingOrder
from log_message_processing import process_data, load_and_split_messages
from utils import remove_columns_with_special_characters, remove_trailing_characters
from date_time_processing import process_time_date_columns
from pid_tid_component_processing import process_component_column_by_pattern, process_pid_column


def apply_functions_to_dataframe(df, functions):
    """
    Applies a list of functions to a DataFrame sequentially.

    Args:
        df (pd.DataFrame): The input DataFrame.
        functions (list): List of functions where each function accepts a DataFrame as input.

    Returns:
        pd.DataFrame: The DataFrame after applying all functions in the list.
    """
    for func in functions:
        if isinstance(func, tuple):
            func_name, kwargs = func[0], func[1]
            func = globals()[func_name]  
            result = func(df, **kwargs)
        else:
            result = func(df)
        
        if isinstance(result, tuple):
            df = result[0]  
        else:
            df = result
    
    return df

def log_parser(log_file_path):
    """
    Process the log file and return a structured DataFrame.

    Args:
        log_file_path (str): The path to the log file.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    training_messages, remaining_messages = load_and_split_messages(log_file_path)
    training_message_texts = [msg for _, msg in training_messages]
    training_df, found_delimiter = process_data(training_message_texts, num_columns=13)
    training_df_log_structurer = LogParsingOrder(training_df)
    structured_training_df, cols_added_num, used_functions = training_df_log_structurer.structure_logs()
    
    structured_training_df_col_count = structured_training_df.shape[1]
    structured_training_df_col_names = structured_training_df.columns

    if remaining_messages:
        remaining_df_cols_num = structured_training_df_col_count - cols_added_num 
        remaining_message_texts = [msg for _, msg in remaining_messages]
        remaining_df, remaining_df_delimiter = process_data(remaining_message_texts, num_columns=remaining_df_cols_num, delimiter=found_delimiter)
        processed_remaining_df = apply_functions_to_dataframe(remaining_df, used_functions)
        processed_remaining_df.columns = structured_training_df_col_names
        structured_training_df['Original_Index'] = [idx for idx, _ in training_messages]
        processed_remaining_df['Original_Index'] = [idx for idx, _ in remaining_messages]
        df_combined = pd.concat([structured_training_df, processed_remaining_df])
        df_combined = df_combined.sort_values('Original_Index').reset_index(drop=True)
        df_combined = df_combined.drop(columns=['Original_Index'])
    else:
        df_combined = structured_training_df.copy()

    df_combined = remove_columns_with_special_characters(df_combined)
    df_cleaned = df_combined.map(remove_trailing_characters)
    return df_cleaned


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Process log files.')
    parser.add_argument('log_file_path', type=str, help='Path to the log file')
    args = parser.parse_args()
    df_cleaned = log_parser(args.log_file_path)


