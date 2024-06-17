"""
Module provides additional functions for text cleaning and data manipulation.
"""

import re
from typing import Any
import json
import numpy as np
import pandas as pd  

def load_json(file_path: str) -> dict:
    """
    Load data from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The data loaded from the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def clean_text_special_signs(text: Any) -> str:
    """
    Clean the input text by removing special signs at the beginning and end.

    Args:
        text (Any): The input text to be cleaned. It can be of any type.

    Returns:
        str: The cleaned text as a string.
    """
    if text is None:
        return ''
    if isinstance(text, float):
        return str(text)
    cleaned_text = text.strip().lower()
    cleaned_text = re.sub(r'^[\[\]:,]+|[\[\]:,]+$', '', cleaned_text)
    return cleaned_text


def lower_strip_text(text: Any) -> str:
    """
    Clean the input text by stripping leading and trailing whitespaces and converting to lowercase.

    Args:
        text (Any): The input text to be cleaned. It can be of any type.

    Returns:
        str: The cleaned text as a string.
    """
    if text is None:
        return ''
    if isinstance(text, float):
        return str(text)
    cleaned_text = text.strip().lower()
    return cleaned_text


def remove_trailing_characters(text: Any) -> str:
    """
    Remove specific trailing characters from the input text.

    Args:
        text (Any): The input text to be cleaned. It can be of any type.

    Returns:
        str: The cleaned text as a string.
    """
    if text is None:
        return ''
    if isinstance(text, float):
        return str(text)
    text = re.sub(r'^[\[,\-]+', '', text)
    text = re.sub(r'[\[\]:,\-@]+$', '', text)
    return text

def drop_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop columns that contain only empty strings or NaN values from a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame to be cleaned.

    Returns:
        pd.DataFrame: The cleaned DataFrame with empty columns dropped.
    """
    columns_to_replace = [col for col in df.columns if df[col].replace(r'^\s*$', np.nan, regex=True).isna().all()]
    
    df[columns_to_replace] = df[columns_to_replace].replace(r'^\s*$', np.nan, regex=True)
    
    df_cleaned = df.dropna(axis=1, how='all')
    
    return df_cleaned


def contains_any(word: str, l1: list) -> bool:
    """
    Check if the input word contains any of the elements in the provided list.

    Args:
        word (str): The word to be checked.
        l1 (list): The list of elements to check against.

    Returns:
        bool: True if any element from the list is found in the word, False otherwise.
    """
    return any(item in word for item in l1)


def remove_pattern(text: str, pattern: str) -> str:
    """
    Remove a specific pattern from the input text.

    Args:
        text (str): The input text to be cleaned.
        pattern (str): The pattern to be removed.

    Returns:
        str: The cleaned text with the pattern removed.
    """
    return re.sub(pattern, '', text).strip()


def matches_pattern(text: str, pattern: str) -> bool:
    """
    Check if the input text matches a specific pattern.

    Args:
        text (str): The input text to be checked.
        pattern (str): The pattern to check against.

    Returns:
        bool: True if the pattern is found in the text, False otherwise.
    """
    return bool(re.search(pattern, text))


def remove_numbers_and_brackets(text: str) -> str:
    """
    Remove numbers and brackets from the input text.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text with numbers and brackets removed.
    """
    if text is None:
        return ''
    text = re.sub(r'^\[', '', text)
    text = re.sub(r'\]:$|:$|]$|@$|:@$', '', text) 
    return text


def is_only_numeric(val):
    """
    Check if the given value contains only numeric characters.

    Args:
        val (str): The value to be checked.

    Returns:
        bool: True if the value contains only numeric characters, False otherwise.
    """
    return bool(re.match(r'^\d+$', str(val)))


def is_only_special(val):
    """
    Check if the given value contains only special characters.

    Args:
        val (str): The value to be checked.

    Returns:
        bool: True if the value contains only special characters, False otherwise.
    """
    return bool(re.match(r'^[\W_]+$', str(val))) 


def remove_columns_with_special_characters(df):
    """
    Remove columns from a DataFrame that contain only special characters.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with specified columns removed.
    """
    for column in df.columns:
        if column.startswith('Col_'):
            if all(df[column].apply(is_only_special)):
                df = df.drop(columns=[column])
    return df




