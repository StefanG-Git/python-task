from typing import List

import pandas as pd


def merge_dataframes(left_df: pd.DataFrame, right_df: pd.DataFrame,
                     merge_type: str, merge_column: str, suffixes: tuple) -> pd.DataFrame:

    new_df = left_df.merge(right_df, how=merge_type, on=merge_column, suffixes=suffixes)

    return new_df


def filter_rows_with_none_values(df: pd.DataFrame, column: str) -> pd.DataFrame:
    new_df = df[df[column].notnull()]

    return new_df


def get_common_columns(first_df: pd.DataFrame, second_df: pd.DataFrame) -> list:
    common_columns = first_df.columns.intersection(second_df.columns).tolist()

    return common_columns


def replace_none_values(df: pd.DataFrame, common_columns: List[str]) -> pd.DataFrame:
    for column in common_columns:
        df[column] = df[column].where(df[column].notnull(), df[column + "_drop"])

    return df


def drop_duplicate_columns(df: pd.DataFrame, common_columns: List[str]) -> pd.DataFrame:
    df = df.drop([c + "_drop" for c in common_columns], axis=1)

    return df


def sort_dataframe(df: pd.DataFrame, sort_columns: str | List[str], ascending: bool | List[bool]) -> pd.DataFrame:
    df = df.sort_values(by=sort_columns, ascending=ascending)

    return df
