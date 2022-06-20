##Telegram OpenSea Bot.


<b>Description.</b>

- Bot should provide an easy way to monitor FP (Floor Price) for NFT collections listed on OpenSea.
- Each user can store as many NFT collection as he would like and recieve either current price by requesting it manually or subscribe to updates.
- Bot has an ability to notify user upon price chnage (based on provided percentage change).


<b>How to install and run Bot.</b>

1. Download all files from repository.
2. Run virtual environment inside of the folder. #python -m venv venv
3. Install required libraries. #pip install -r requirements.txt
4. In order to be bale to update user you should run main.py and monitor_price.py.


<b>How to use.</b>

- During first interaction with this bot (assuming nothing was saved for particular user), only one option will appear - Add Collection.
- User has two options:
  - Provide name of NFT collection only. (will not get automatic updates)
  - Provide name of NFT collection along with percentage - price movements.
- At this point, user should see one more option such as 'Get price'.


<b>Examples.</b>

1. In order to start bot, type '/start'
2. Now you have to options, provide only NFT collection name OR NFT collection + percentage.
  1. Name of NFT collection should be taken from OpenSea URL. https://opensea.io/collection/goblintownwtf 
  In this example NFT collection will be - 'goblintownwtf'
  2. Second option is to provide NFT collection name + interested price change.
  goblintownwtf 15
  Above example means that this particular user will get notifications every time FP price of 'goblintownwtf' changes (+15% or -15%)
3. There is also an option to get price for all saved collection - Get Price. (will fetch FP price for all collections user added)
  


<b>How it works.<b>
  
  
db_service
  
Creates on table with below columns:
  - chat_id (telegram chat id, unique per user)
  - name (name of telegram user, can be not unique)
  - collection (NFT collection added by user)
  - current_price (FP for NFT collection)
  - percentage (by default 0, on what FP change update user)
  - timestamp (updated everytime when FP was updated)
  
  
api_os.py
  
Makes API calls to OpenSea:
  - get_price. Fetch current FP for particular collection - "https://api.opensea.io/api/v1/collection/" + collection name
  - check_collection. Fetch collection name from OpenSea in order to verify if name is correct and exists.
  
  
main.py
  

  

