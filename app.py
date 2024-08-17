import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes and converting to string:
    data = uploaded_file.getvalue().decode('utf-8')
    df = preprocessor.preprocessor(data)
    
    # Fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    
    selected_user = st.sidebar.selectbox('Analysis for', user_list)
    if st.sidebar.button('Show Analysis'):

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total messages')
            st.write(num_messages)
        with col2:
            st.header('Total words typed')
            st.write(words)
        with col3:
            st.header('Shared media')
            st.write(num_media_messages)
        with col4:
            st.header('Shared links')
            st.write(num_links)
        
        # Monthly timeline
        st.title('Monthly timeline')

        timeline, time = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time, timeline['message'], color = 'yellow')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Activity map
        st.title('Activity map')
        col1, col2 = st.columns(2)

        with col1:
            # Day
            st.header('Busy day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'red')
            plt.xticks(rotation = 25)
            st.pyplot(fig)
        with col2:
            # Month
            st.header('Busy month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        # Heatmap
        st.title('Hour activity')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Busy users
        if selected_user == 'Overall':
            st.title('Most busy users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color = 'violet')
                plt.xticks(rotation = 45)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # Wordcloud
        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Common words
        st.title('Most common words')
        most_common_df = helper.most_used_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df['word'], most_common_df['count'], color = 'indigo')
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title('Emojis')

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct = '%.2f%%')
            st.pyplot(fig)