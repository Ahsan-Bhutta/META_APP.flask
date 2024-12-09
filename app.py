from flights import get_flights
import json
from flask import Flask, render_template, request, Response, jsonify
from message_helper import get_templated_message_input, get_text_message_input, send_message
import flask
from message_helper import get_text_message_input, send_message 
 
app = Flask(__name__)
 
with open('config.json') as f:
    config = json.load(f)

app.config.update(config)

@app.route("/")
def index():
    return render_template('index.html', name=__name__)

@app.route('/welcome', methods=['POST'])
async def welcome():
  data = get_text_message_input(app.config['RECIPIENT_WAID']
                                , 'Welcome to the Flight Confirmation Demo App for Python!');
  await send_message(data)
  return flask.redirect(flask.url_for('catalog'))

@app.route("/catalog")
def catalog():
    return render_template('catalog.html', title='Flight Confirmation Demo for Python', flights=get_flights())

@app.route("/buy-ticket", methods=['POST'])
async def buy_ticket():
  flight_id = int(request.form.get("id"))
  flights = get_flights()
  flight = next(filter(lambda f: f['flight_id'] == flight_id, flights), None)
  data = get_templated_message_input(app.config['RECIPIENT_WAID'], flight)
  await send_message(data)
  return flask.redirect(flask.url_for('catalog'))

@app.route("/webhook", methods=['GET'])
def waqar_webhook():
  # Retrieve the verification parameters
  hub_mode = request.args.get('hub.mode')
  hub_challenge = request.args.get('hub.challenge')
  hub_verify_token = request.args.get('hub.verify_token')
  # Validate the token
  if hub_verify_token == "happyhappy":
      if hub_mode == 'subscribe':
          return Response(hub_challenge, status=200)  # Return the challenge string back to WhatsApp
      else:
          return Response("Invalid hub.mode", status=400)
  else:
      return Response("Invalid verify token", status=403)  # Unauthorized if token is incorrect


@app.route('/webhook', methods=['POST'])
async def webhook():
  if request.is_json:
      data = request.get_json()
      if 'entry' in data:
          for entry in data['entry']:
              if 'changes' in entry:
                  for change in entry['changes']:
                      if 'value' in change:
                          messages = change['value'].get('messages', [])
                          if messages:
                              for message in messages:
                                from_number = message.get('from')  # Sender's phone number
                                user_message = message.get('text', {}).get('body')  # Message body
                                # Example icebreakers (replace with your actual icebreakers)
                                ICEBREAKERS_RESPONSES = {
                                    "Help to create a lesson plan for me": "Physics, Chemistry, or Biology.",
                                    "Test my understanding": "Our latest products are available here: [https://wapp.ap.ngrok.io/catalog]",
                                    "Watch a video to practice listening comprehension": "Sure, to track your order, please provide your order number.\n This is the video link :[https://youtu.be/iotXlNhAwRA] ",
                                    "Offer study materials for my exam": "Here are some resources to help to you prepare my study links : [https://www.tutorialsduniya.com/cbse/ncert-books/]."
                                }
                                bot_message = ICEBREAKERS_RESPONSES.get(user_message)
                                if bot_message:                                    
                                    bot_message_response = get_text_message_input(app.config['RECIPIENT_WAID'], bot_message);
                                    await send_message(bot_message_response)
                                    print("This is my bot_message",bot_message)
                                elif user_message == "Physics":
                                    bot_message = "Physics is a great choice!\n\nIt's the language of the universe, unraveling the mysteries of matter, energy, and space-time."
                                    bot_message_response = get_text_message_input(app.config['RECIPIENT_WAID'], bot_message)
                                    await send_message(bot_message_response)    
                                elif user_message == "Chemistry":
                                    bot_message = "Chemistry is a great choice!\n\nThe science of change, where atoms dance and molecules transform, painting the world with vibrant hues and intricate patterns."
                                    bot_message_response = get_text_message_input(app.config['RECIPIENT_WAID'], bot_message)
                                    await send_message(bot_message_response)    
                                elif user_message == "Biology":
                                    bot_message = "Biology is a great choice!\n\nThe symphony of life, where cells compose the music of existence, and evolution orchestrates the grand spectacle of biodiversity."
                                    bot_message_response = get_text_message_input(app.config['RECIPIENT_WAID'], bot_message)
                                    await send_message(bot_message_response)                 
                                else:
                                    bot_message = "Thanks for response.I can further assist you Tommorow!\nI'll be available to provide more detailed information or answer any questions you may have."
                                    bot_message_response = get_text_message_input(app.config['RECIPIENT_WAID'], bot_message)
                                    await send_message(bot_message_response)
      return jsonify({"status": "success"}), 200
  else:
      return jsonify({"error": "Invalid request format"}), 400








