from typing import List, Dict, Any

import pandas as pd

from utils.request_utils import get_request_resource


def merge_dataframes(left_df: pd.DataFrame, right_df: pd.DataFrame,
                     merge_type: str, merge_columns: str | List[str], suffixes: tuple) -> pd.DataFrame:
    """
    Merge two dataframes by given columns.

    Parameters
    ----------
    left_df : pd.DataFrame
        First DataFrame to merge.
    right_df : pd.DataFrame
        Second DataFrame to merge with.
    merge_type : str
        How to merge the two DataFrames.
    merge_columns: str
        Columns names to join on.
    suffixes : tuple
        String indicating the suffix to add to overlapping column names in left and right respectively.

    Returns
    -------
    new_df : pd.DataFrame
        The merged DataFrame.
    """
    new_df = left_df.merge(right_df, how=merge_type, on=merge_columns, suffixes=suffixes)

    return new_df


def filter_rows_with_none_values(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Remove rows from DataFrame where value from given column is Null.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to filter.
    column : str
        Column name to use for filtering.

    Returns
    -------
    new_df : pd.DataFrame
        The filtered DataFrame.
    """
    new_df = df[df[column].notnull()]

    return new_df


def get_common_columns(first_df: pd.DataFrame, second_df: pd.DataFrame) -> list:
    """
    Find the common column names from two DataFrames.

    Parameters
    ----------
    first_df : pd.DataFrame
        First DataFrame to compare.
    second_df : pd.DataFrame
        Second DataFrame to compare.

    Returns
    -------
    common_columns : list
        List with the common column names.
    """
    common_columns = first_df.columns.intersection(second_df.columns).tolist()

    return common_columns


def replace_null_values(df: pd.DataFrame, common_columns: List[str]) -> pd.DataFrame:
    """
    Compare the generated columns from DataFrame after merge
    and check if one is Null, then takes the value from the other.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to use for replacing the values.
    common_columns : List[str]
        List with column names to compare.

    Returns
    -------
    df : pd.DataFrame
        DataFrame with replaced values.
    """
    for column in common_columns:
        df[column] = df[column].where(df[column].notnull(), df[column + "_drop"])

    return df


def drop_suffix_columns(df: pd.DataFrame, columns: List[str], suffix: str) -> pd.DataFrame:
    """
    Drop redundant columns from DataFrame generated after merge.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to use for dropping the columns.
    columns : List[str]
        List with column names to drop.
    suffix : str
        Suffix extension of the redundant columns

    Returns
    -------
    df : pd.DataFrame
        DataFrame without redundant columns.
    """
    new_df = df.drop([f"{c}{suffix}" for c in columns], axis=1)

    return new_df


def drop_mismatch_columns(df: pd.DataFrame, columns: List[str]):
    """
    Compare and drop columns from DataFrame
    that are not in the given list.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to use for dropping the columns.
    columns : List[str]
        List with column names to compare.

    Returns
    -------
    df : pd.DataFrame
        DataFrame without the columns that are not in the list.
    """
    new_df = df.drop(df.columns.difference(columns, sort=False), axis=1)

    return new_df


def sort_dataframe(df: pd.DataFrame, sort_columns: str | List[str], ascending: bool | List[bool]) -> pd.DataFrame:
    """
    Sort DataFrame by given columns in given order.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to sort.
    sort_columns : List[str]
        List with column names to use for sorting.
    ascending: bool
        How to sort the DataFrame.

    Returns
    -------
    df : pd.DataFrame
        Sorted Dataframe.
    """
    new_df = df.sort_values(by=sort_columns, ascending=ascending)

    return new_df


def add_new_column(df: pd.DataFrame, column_name: str, value: Any = None):
    """
    Add new column in DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame use for adding the new column.
    column_name : str
        Name of the new column.
    value: Any
        Value to add in the new column.

    Returns
    -------
    df : pd.DataFrame
        Dataframe with the new column.
    """
    df[column_name] = value

    return df
