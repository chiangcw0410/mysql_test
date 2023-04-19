# Importing required packages
import streamlit as st
import openai

st.title("Chatting with ChatGPT")
st.sidebar.header("Instructions")
st.sidebar.info(
    '''This is a web application that allows you to interact with 
       the OpenAI API's implementation of the ChatGPT model.
       Enter a **query** in the **text box** and **press enter** to receive 
       a **response** from the ChatGPT
       '''
    )

# 設置模型引擎和您的 OpenAI API 密鑰
model_engine = "text-davinci-003"
"""
openai.api_key = "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"  #按照第 4 步獲取 secret_key



def main(): 
    
    # 此函數獲取用戶輸入，將其傳遞給 ChatGPT 函數並
    # 顯示響應
    
    # 獲取用戶輸入
    user_query = st.text_input( "Enter query here, to exit enter :q" , "what is Python?" ) 
    if user_query != ":q"  or user_query != "" : 
        # 將查詢傳遞給 ChatGPT 函數
        response = ChatGPT(user_query) 
        return st.write( f" {user_query}  {response} " )
    

def ChatGPT(user_query):
    
    # This function uses the OpenAI API to generate a response to the given 
    # user_query using the ChatGPT model
    
    # Use the OpenAI API to generate a response
    completion = openai.Completion.create(
                                  engine = model_engine,
                                  prompt = user_query,
                                  max_tokens = 1024,
                                  n = 1,
                                  temperature = 0.5,
                                      )
    response = completion.choices[0].text
    return response


# 調用主函數
main()

"""
