def merge_dataframes(left_df, right_df, merge_type, merge_column, suffixes):
    new_df = left_df.merge(right_df, how=merge_type, on=merge_column, suffixes=suffixes)

    return new_df


def filter_rows_with_none_values(df, column):
    new_df = df[df[column].notnull()]

    return new_df


def get_common_columns(first_df, second_df):
    common_columns = first_df.columns.intersection(second_df.columns).tolist()

    return common_columns


def replace_none_values(df, common_columns):
    for column in common_columns:
        df[column] = df[column].where(df[column].notnull(), df[column + "_drop"])

    return df


def drop_duplicate_columns(df, common_columns):
    df = df.drop([c + "_drop" for c in common_columns], axis=1)

    return df
