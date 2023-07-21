# write a single-page website, that there is a text input box.
# The user can input a piece of text, and then we display a 
# word-frequency table and word cloud regarding to the text.

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import wordcloud

def create_link(url:str) -> str:
    return f'''<a href="{url}">🔗</a>'''


# Title
st.title('Word Frequency Analysis by Future')

# Input box
user_input = st.text_area('Input your text here. We won\'t save your text:', value='', height=200)
user_input = user_input.lower()

# Button
if st.button('Analyze'):
    if not user_input:
        st.warning('Please input your text!')
        st.stop()
    words = user_input.split()

    # move the punctuation
    words = [word.strip('.,!;:()[]"') for word in words]

    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    # First, show the total number of words, total number of distinct words, and distinct ratio here
    # bold font
    st.text(f'Total number of words: {len(words)}, ')
    st.text(f'total number of distinct words: {len(word_freq)}, ')
    st.text(f'distinct ratio: {len(word_freq)/len(words)*100:.2f}%')

    word_freq = pd.DataFrame.from_dict(word_freq, orient='index', columns=['Frequency'])
    word_freq.index.name = 'Word'
    word_freq = word_freq.sort_values(by='Frequency', ascending=False)

    # print(word_freq)

    # show word cloud
    wc = wordcloud.WordCloud(width=1000, height=600, background_color='white')
    wc.fit_words(word_freq['Frequency'])
    st.image(wc.to_array())

    # show table with st.DataFrame, set height for the total number of elements
    # st.dataframe(word_freq, use_container_width=True, height=1000)

    # add a new column, the link to https://www.thesaurus.com/browse/{}
    word_freq['Synonum'] = [create_link(f'https://www.thesaurus.com/browse/{word}') for word in word_freq.index.to_list()]
    
    # make the word column as the first column
    word_freq.insert(0, 'Word', word_freq.index)

    print(word_freq)
    fig = go.Figure(
        data=[
            go.Table(                
                columnwidth = [1,1,0.5],
                header=dict(
                    values=[f"<b>{i}</b>" for i in word_freq.columns.to_list()],
                    fill_color='orange'
                    ),
                cells=dict(
                    values=word_freq.transpose(),
                    font=dict(size=20),
                    ),
                ),
            ]
        )
    fig.update_layout(height=1000)

    st.text('The table below shows the frequency of each word and the link to its synonum:')

    st.plotly_chart(fig, use_container_width=True)
