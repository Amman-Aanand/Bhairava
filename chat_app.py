import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Bhairava", page_icon="R.png")

Langchain_API_KEY = st.secrets["LANGCHAIN_API_KEY"]
Groq_API_KEY = st.secrets["GROQ_API_KEY"]

# Particle.js background
particles_js = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js</title>
  <style>
  #particles-js {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    z-index: -1; /* Send the animation to the back */
  }
  .content {
    position: relative;
    z-index: 1;
    color: white;
  }
  </style>
</head>
<body>
  <div id="particles-js"></div>
  <div class="content">
    <!-- Placeholder for Streamlit content -->
  </div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 300,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          },
          "image": {
            "src": "img/github.svg",
            "width": 100,
            "height": 100
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.2,
            "sync": false
          }
        },
        "size": {
          "value": 2,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#ffffff",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 0.2,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": true,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 2,
            "duration": 2,
            "opacity": 0.5,
            "speed": 1
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 2
          },
          "remove": {
            "particles_nb": 3
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""

# Inject the particle animation HTML into the Streamlit app
st.components.v1.html(particles_js, height=0)

# Main content of the Streamlit app
st.title("Bhairava :trident:")
st.write("नमस्कार!🙏")

models = ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "llama3-groq-70b-8192-tool-use-preview", 
          "llama3-groq-8b-8192-tool-use-preview"]


st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #2E4053;
        color: white;
        font-family: 'Courier New', Courier, monospace;
    }
    .sidebar .sidebar-content h2 {
        font-size: 1.5em;
        font-weight: bold;
        color: #F7DC6F;
    }
    .sidebar .sidebar-content select {
        background-color: #F7DC6F;
        color: #2E4053;
        font-weight: bold;
        border-radius: 5px;
        padding: 5px;
        font-size: 1.1em;
    }
    </style>
""", unsafe_allow_html=True)

# Create the sidebar header with custom styling
st.sidebar.header("🔍 Choose Your LLM Model:")
st.sidebar.write("**Explore the available models and pick the one that suits your needs.**")

# Add a creative description or instructions
st.sidebar.info("🌟 *Tip*: For faster responses, select the **instant** models. For more detailed insights, go for the **versatile** ones.")

# Enhanced selectbox with a unique label and style
model = st.sidebar.selectbox(
    label="🧠 **Pick your model:**",
    options=models,
    index=2
)

# Display the selected model in a creative way
st.sidebar.write(f"**You’ve chosen:** `{model}`")

clicked = st.sidebar.button("Clear Chat History")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are helpful assistant pretending to be Bhairava"),
        ("placeholder","{Chat_history}"),
        ("user","{query}"),
    ]
)

llm = ChatGroq(model=model) #temperature=temperature

chain = prompt | llm | StrOutputParser()

msgs = StreamlitChatMessageHistory()
if len(msgs.messages) ==0 or clicked:
    msgs.clear()
    msgs.add_ai_message(chain.invoke(
        {"query": "Write a brief welcome message",
         "chat_history":[]
         }

    ))

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="query",
    history_messages_key="chat_history",
)

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)


chat_input = st.chat_input("“अपना प्रश्न पूछें”।   Please ask your Question ")

if chat_input:
    config = {"configurable": {"session_id" :"any"}}
    response = chain_with_history.invoke({"query": chat_input}, config)
    st.chat_message("user").write(chat_input)
    st.chat_message("au").write(response)
    #st.write(llm.model_name)
