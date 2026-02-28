import os
from langchain_core.prompts import ChatPromtTemplate
# if you're on raspberry pi or sum do this if you want it to interact with electronics
import RPi.GPIO as GPIO
import time

template = """

# your template goes here (basically the instructions on how the bot should interact/answer questions)
example is "you are a helpful home assistant, answer all questions to your best ability
 
this is the question: {question}

here is the short term conversation history: {context}

answer:
"""

def load_memory():
  memory_dir = "folder you want to put it in" # for example /home/billybob/AI_memory
  memories = []
  for filename in os.listdir(memory_dir):
    with open(os.path.join(memory_dir, filename), "r", encoding="utf-8") as f:
      memories.append(f.read())
  return "\n---\n".join(memories)

def save_memory(context, question, AI_memory):
  memory_dir = "same file as load_memory"
  if not os.path.exists(memory_dir):
    os.makedirs(memory_dir)
  filepath = os.path.join(memory_dir, f"{AI_memory}.md")
  with open(filepath, "w", encoding="utf-8") as f:
    f.write(f"Context: {context}\nQuestion: {question}")
  return f"Memory saved to {filepath}"

AI_memory = "folder that memory is in"

running = True

while running:

  def loop():

    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="the model u want")
    chain = prompt | model

    context = ""
    Memory = load_memory()
    user_input = input("Enter your prompt: ")
    result = chain.invoke({"Memory": Memory, "context": context, "question": user_input})

    print("bot: " result)
    context += f" {user_input} {result}"
    save_memory(context, user_input, AI_memory)
    return loop()

  loop()
