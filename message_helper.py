import aiohttp
import json
from flask import current_app

async def send_message(data):
  headers = {
    "Content-type": "application/json",
    "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }
    
  async with aiohttp.ClientSession() as session:
    url = 'https://graph.facebook.com' + f"/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"
    try:
      async with session.post(url, data=data, headers=headers) as response:
        if response.status == 200:
         html = await response.json()
        else:
          print(response.status)        
    except aiohttp.ClientConnectorError as e:
      print('Connection Error', str(e))


def get_text_message_input(recipient, text):
  return json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": recipient,
    "type": "text",
    "text": {
      "preview_url": False,
      "body": text
    }
  })


def get_templated_message_input(recipient, flight):
  return json.dumps({
    "messaging_product": "whatsapp",
    "to": recipient,
    "type": "template",
    "template": {
      "name": "purchase_receipt_1",
      "language": {
        "code": "en_US"
      },
      "components": [
        {
          "type": "header",
          "parameters": [
            {
              "type": "document",
              "document": {
                "filename": "FlightConfirmation.pdf",
                "link": flight['document']
              }
            }
          ]
        },
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": flight['origin']
            },
            {
              "type": "text",
              "text": flight['destination']
            },
            {
              "type": "text",
              "text": flight['time']
            }
          ]
        }
      ]
    }
  })

