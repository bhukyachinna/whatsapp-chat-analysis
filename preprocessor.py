import re
import pandas as pd

def preprocessor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Preparing a Dataframe
    df = pd.DataFrame({'user_message' : messages, 'date' : dates})
    df.date = pd.to_datetime(df.date, format = '%d/%m/%Y, %H:%M - ')

    # Splitting message and users
    users = []
    messages = []
    for message in df.user_message:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])        

    df['user'] = users
    df['message'] = messages
    df.drop(columns = 'user_message', inplace = True)

    df['year'] = df.date.dt.year
    df['month_num'] = df.date.dt.month
    df['month'] = df.date.dt.month_name()
    df['day'] = df.date.dt.day
    df['hour'] = df.date.dt.hour
    df['minute'] = df.date.dt.minute
    df['day_name'] = df.date.dt.day_name()

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(0) + str(hour + 1))
        elif hour == 9:
            period.append(str(0) + str(hour) + '-' + str(hour + 1))
        elif hour < 9:
            period.append(str(0) + str(hour) + '-' + str(0) + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period

    return df