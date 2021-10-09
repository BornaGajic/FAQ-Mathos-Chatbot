# FAQ-Mathos-Chatbot
Chatbot created with [Rasa framework](https://rasa.com/)  
Try it out on Telegram, [here](https://t.me/faq_mathos_bot)

### Commands
 * Open the 5005 port
`./ngrok http 5005`
 * Connect with Telegram  
`rasa run --connector telegram --model models --enable-api --cors "*" -v -vv`
 * Run action server
`rasa run actions`
