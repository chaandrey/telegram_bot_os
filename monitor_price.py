import db_service, api_os, send_msg
import time, datetime


while True:
    user = db_service.get_users_for_update()
    if user:
        print(user)
        current_price = api_os.get_price(user[2])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if current_price % user[3] > user[3] * (user[4] / 100):
            message = 'Price for {} was chnaged, from {} to {}'.format(user[2], user[3], current_price)
            send_msg.send_msg(user[0], message)
            print(user[0], user[2], current_price)
        db_service.update_record(user[0], user[2], current_price, timestamp)
    time.sleep(15)