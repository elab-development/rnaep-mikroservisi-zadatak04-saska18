import time
import os
from redis_om import get_redis_connection
from dotenv import load_dotenv

load_dotenv()

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def process_notifications():
    print("Notification servis pokrenut...")
    while True:
        try:
            results = redis.xread({"order_completed": "$", "refund_order": "$"}, block=5000, count=1)
            if results:
                for stream_name, messages in results:
                    for msg_id, data in messages:
                        order_id = data.get('pk', 'Nepoznato')
                        if stream_name == "order_completed":
                            print(f"--- OBAVEŠTENJE: Porudžbina {order_id} je PLAĆENA. ---")
                        elif stream_name == "refund_order":
                            print(f"--- OBAVEŠTENJE: Porudžbina {order_id} je REFUNDIRANA. ---")
        except Exception as e:
            print(f"Greška: {e}")
            time.sleep(2)

if __name__ == "__main__":
    process_notifications()