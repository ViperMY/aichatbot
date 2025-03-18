import streamlit as st
import requests
from pygments.lexers import guess_lexer, ClassNotFound
import configparser
import sidebar

config = configparser.ConfigParser()
config.read("config.ini")

def is_code_pygments(text):
    try:
        guess_lexer(text)
        return True
    except ClassNotFound:
        return False

def initMsgHistory():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []

def showMsgHistory():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if is_code_pygments(message["content"]) == True and message["role"] == "user":
                st.code(message["content"])
            else:
                st.markdown(message["content"])

def layout():
    #sidebar
    st.markdown("""
        <style>
                .st-emotion-cache-16txtl3 {
                    padding-top: 3rem; 
                    padding-bottom: 0rem; 
                    padding-left: 1.5rem; 
                    padding-right: 1.5rem;
                }
                
                .stDeployButton {visibility: hidden;}
                .st-emotion-cache-15zrgzn {display: none}
                .st-emotion-cache-gi0tri {display: none}
        </style>
        """, unsafe_allow_html=True)
    
    # 重啟對話按鈕
    sidebar.addResetBtn()
    
    # 分隔線
    sidebar.addSeparator()

    # AI參數
    with st.sidebar:
        st.subheader("AI參數")

    # 選擇角色
    role = sidebar.addRoleSelect()
    role = "聊天機器人" if role == "其他" else role
    
    # 選擇model
    secondModelChoice = sidebar.addModelSelect()

    # 溫度選擇
    temperature = sidebar.addTemperatureSelect()

    # 回應的最大token字數數量限制
    # maxTokenLimit = addMaxTokenLimit()

    with st.sidebar:
        st.caption("Temperature - 對於非創造性任務（翻譯、分類提取、標準化、格式轉換、語法修復）和嚴格遵守說明，優選溫度為0或最高0.3。對於更具創造性的任務，您應該將溫度調高，接近0.5。如果您希望具有高度創造性（例如，對於行銷或廣告文案），請考慮0.7到1之間的值，但要小心並檢查結果是否有幻覺。")
                #    \\r\n\r\nMax tokem - 模型回應的最大token字數數量限制，假如你不想要回應太長，可以設定這個值")
    # AI參數 END
    #sidebar END
    
    st.title("AI聊天機器人")
    st.caption("什麼都可以問💬但我不一定會答😜")
    
    # 初始化聊天記錄
    initMsgHistory()
    
    # 顯示聊天記錄
    showMsgHistory()
    
    startChat(secondModelChoice, temperature, role)

def startChat(secondModelChoice, temperature, role):
    # 使用者輸入
    if prompt := st.chat_input("請輸入您的訊息"):
        
        # 歷史內容
        msgHistory = ""
        st.session_state.history = []
        for msg in st.session_state.history:
            msgHistory += f"{msg}\n"

        requestPrompt = f"""你是一個{role}，請依照以下規則處理對話：
                            - 使用繁體中文(zhtw)
                            - 使用口語化但得體的表達方式
                            - 使用台灣常用的口語,而非中國常用的口語
                        以下是歷史對話記錄：
                        {msgHistory}
                        以下是使用者新輸入的對話內容：{prompt}
                        請依照歷史對話紀錄與使用者輸入內容來回答或處理"""
        
        # 多一筆輸入訊息到聊天記錄
        st.session_state.messages.append({"role": "user", "content": prompt})
        # 新增使用者歷史訊息
        st.session_state.history.append("使用者: " + prompt)

        with st.chat_message("user"):
            if is_code_pygments(prompt) == True:
                st.code(prompt)
            else:
                st.markdown(prompt)

        # 打Bedrock api
        apiUrl = config["apis"]["bedrockApi"]
        
        with st.chat_message("ai"):
            with st.spinner("思考中..."):
                try:
                    payload = {
                        "input": requestPrompt,
                        "model_id": secondModelChoice,
                        "temperature": float(temperature),
                        # "max_token": int(maxTokenLimit)
                    }
                    
                    # request
                    response = requests.post(
                        apiUrl,
                        json=payload
                    )
                    
                    # check status
                    try:
                        response.raise_for_status()
                    except requests.exceptions.HTTPError as e:
                        # not 200
                        print("Error: " + str(e))
                    
                    result = response.json()
                    
                    # show msg
                    if "response" in result:
                        st.markdown(result["response"])
                        # 多一筆回應到聊天紀錄
                        st.session_state.messages.append(
                            {"role": "ai", "content": result["response"]}
                        )
                        # 新增AI歷史訊息
                        st.session_state.history.append("AI: " + result["response"])
                    else:
                        st.error("Response error")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"API request ERROR: {str(e)}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    layout()
