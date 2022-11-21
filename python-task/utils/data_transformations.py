def merge_dataframes(left_df, right_df, merge_type, merge_column):
    new_df = left_df.merge(right_df, how=merge_type, on=merge_column)

    return new_df