import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    df = df.pivot(index = "id_1",columns ="id_2", values = "car")
    for  i in df.columns:
        df.loc[i,i] = 0   #diagonal value should be zero we can do this with fillna function also because NA values are coming in the diagonal 

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    from collections import Counter
    type1 = []
    for i in df["car"].values:
        if i<=15:
            type1.append("low")

        elif 15<i<=25:
            type1.append("medium")

        else:
            type1.append("high")
    
    type_count = Counter(type1)
    sorted_type_count = sorted(type_count.items())



    return dict(sorted_type_count)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    mean_value = df["bus"].mean()
    indexes = df[df["bus"] > 2 * mean_value].index.values
    

    return list(indexes)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    filter_data = df.groupby("route")["truck"].mean().reset_index()
    filter_data = filter_data[filter_data["truck"]>7]
    sorted_list = filter_data["route"].sort_values().values

    return list(sorted_list)


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    


    matrix = matrix.applymap(lambda x: round(x * 0.75, 1) if x > 20 else round(x * 1.25, 1))


    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')
    grouped = df.groupby(['id', 'id_2'])
    
    completeness_check = grouped.apply(lambda group: not (
        group['start_timestamp'].min().time() == pd.Timestamp('00:00:00').time() and
        group['end_timestamp'].max().time() == pd.Timestamp('23:59:59').time() and
        set(group['start_timestamp'].dt.dayofweek.unique()) == set(range(7))
    )).reset_index(drop=True)

    return pd.Series(completeness_check)
