from flask import Flask, request, jsonify, render_template
from threading import Thread
import openai
import os

keep_context = "yes"
writing = "yes"


def readchat(file):
  pr = open(file, "r")
  l = pr.readlines()
  str1 = ""
  for ele in l:
    str1 += ele
  pr.close()
  return str1


def writechat(conv):
  pr = open("chats/chat.txt", "a+")
  pr.writelines(conv)
  pr.close()
  tr = open("chats/trashed.txt", "a+")
  tr.writelines(conv)
  tr.close()

def rewrite():
  og = open("chats/chatoriginal.txt", "r")
  ww = open("chats/chat.txt", "w")
  ww.write(og.read())
  print("rewrite")
  l = open("chats/log.txt", "a")
  l.write("\nrewrite")

app = Flask(__name__)
try:
  openai.api_key = os.environ['keyy']
except:
  openai.api_key = input("input api key:")
rewrite()

@app.route("/")
def index():
  return render_template("result.html")


@app.route("/get")
def get_bot_response():
  if keep_context == "yes":
    chatlog = readchat("chats/chat.txt")
  else:
    chatlog = readchat("chats/chatoriginal.txt")
  userText = request.args.get('msg')
  response = openai.Completion.create(engine="text-curie-001",
                                      prompt=(chatlog + "\nHuman:" + userText +
                                              "\nAI:"),
                                      temperature=0.75,
                                      max_tokens=150,
                                      top_p=1,
                                      frequency_penalty=0,
                                      presence_penalty=0.6,
                                      stop=[" Human:", " AI:"])
  output1 = response['choices'][0]['text']
  output = output1.strip()
  print("\nHuman:" + userText + "\nAI:" + output)
  if writing == "yes":
    writechat("\nHuman:" + userText + "\nAI:" + output)
  return output


def keep_alive():
  server = Thread(target=run)
  server.start()


def run():
  app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080, debug=True)
