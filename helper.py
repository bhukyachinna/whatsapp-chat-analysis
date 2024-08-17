from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # 1. Fetch no.of messages
    num_messages = df.shape[0]
    # 2. Fetch no.words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # 3. Fetch no.of media
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4. Fetch no.of links shared
    links = []
    extract = URLExtract()
    for msg in df.message:
        links.extend(extract.find_urls(msg))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df.user.value_counts().head()
    new_df = round((df.user.value_counts() / df.shape[0] * 100), 2).reset_index().rename(
        columns = {'user' : 'name', 'count' : 'percent'})
    return x, new_df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    wc = WordCloud(width = 500, min_font_size = 10, background_color = 'white')
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    temp['message'] = temp['message'].str.lower()

    df_wc = wc.generate(temp['message'].str.cat(sep = ' '))
    return df_wc

def most_used_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns = ['word', 'count'])
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df.message:
        lst = emoji.emoji_list(message)
        for i in lst:
            emojis.extend(i['emoji'])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    
    return timeline, time

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    desired_hours = ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09',
                    '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
                    '18-19', '19-20', '20-21', '21-22', '23-00']
    user_heatmap = df.pivot_table(index = 'day_name', columns = 'period', values = 'message', aggfunc = 'count').fillna(0)
    user_heatmap = user_heatmap.reindex(columns = desired_hours)

    return user_heatmap