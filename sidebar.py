import streamlit as st

def addRoleSelect():
    with st.sidebar:
        return st.selectbox(
            "選擇發問場景",
            (
                "軟體工程師",
                "硬體工程師",
                "後端工程師",
                "前端工程師",
                "資料分析師",
                "系統架構師",
                "技術支援人員",
                "專案經理",
                "產品經理",
                "行銷策略師",
                "行銷人員",
                "教育訓練師",
                "客服人員",
                "其他"
            ),
        )
    
def addModelSelect():
    with st.sidebar:
        modelOptions = {
            "Claude": {
                # "apac claude 3.5 sonnet v1.0": "apac.anthropic.claude-3-5-sonnet-20240620-v1:0", 
                # "apac claude 3 sonnet v1.0": "apac.anthropic.claude-3-sonnet-20240229-v1:0", 
                # "apac claude 3 haiku v1.0": "apac.anthropic.claude-3-haiku-20240307-v1:0", 
                # "us claude 3 haiku v1.0": "us.anthropic.claude-3-haiku-20240307-v1:0", 
                # "us claude 3 opus v1.0": "us.anthropic.claude-3-opus-20240229-v1:0", 
                # "us claude 3 sonnet v1.0": "us.anthropic.claude-3-sonnet-20240229-v1:0", 
                "Claude 3.5 haiku": "us.anthropic.claude-3-5-haiku-20241022-v1:0", 
                "Claude 3.5 sonnet": "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            },
            "Amazon nova": {
                "Nova lite": "us.amazon.nova-lite-v1:0", 
                # "nova pro v1.0": "us.amazon.nova-pro-v1:0", 
                # "nova micro v1.0": "us.amazon.nova-micro-v1:0"
            },
            "Meta llama": {
                # "Llama3.1 70b instruct v1:0": "us.meta.llama3-1-70b-instruct-v1:0", 
                # "Llama3.2 1b instruct v1:0": "us.meta.llama3-2-1b-instruct-v1:0", 
                # "llama3.2 11b instruct v1:0": "us.meta.llama3-2-11b-instruct-v1:0", 
                "Meta llama3.3 70b": "us.meta.llama3-3-70b-instruct-v1:0"
            },
            "DeepSeek": {
                "DeepSeek R1": "us.deepseek.r1-v1:0"
            }
        }
        modelChoice = "Claude"
        modelChoice = st.selectbox("Model", list(modelOptions.keys()))
        versionChoice = st.selectbox("Version", modelOptions[modelChoice])
        modelVersion = modelOptions[modelChoice][versionChoice]

        return modelVersion
    
def addTemperatureSelect():
    with st.sidebar:
        return st.select_slider(
            "Temperature",
            options=[
                "0.0",
                "0.1",
                "0.2",
                "0.3",
                "0.4",
                "0.5",
                "0.6",
                "0.7",
                "0.8",
                "0.9",
                "1.0"
            ],
            value= "0.5"
        )

def addMaxTokenLimit():
    with st.sidebar:
        return st.text_input("Max token", "50")
    
def addResetBtn():
    with st.sidebar:
        if st.button("重啟對話", type="primary", use_container_width=True):
            st.write("將清空對話，是否確認重啟?")
            col1, col2 = st.columns([1,1])

            with col1:
                st.button(
                    label="Ok",
                    on_click=resetMsgeHistory,
                )
            with col2:
                st.button('Cancel')            

def resetMsgeHistory():
    st.session_state.messages = []
    st.session_state.history = []
    
def addSeparator():
    with st.sidebar:
        st.markdown("""<hr style="margin: 1em 0px;height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True) 
