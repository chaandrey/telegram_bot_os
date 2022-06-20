import db_service, api_os, main
import time


while True:
    user = db_service.get_users_for_update()
    if user:
        current_price = api_os.get_price(user[2])
        if current_price % user[3] > user[3] * (user[4] / 100):
            message = 'Price for {} was chnaged, from {} to {}'.format(user[2], user[3], current_price)
            main.send_message(user[0], message)
            db_service.update_record()
    time.sleep(10)