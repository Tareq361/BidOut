from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from GrowexoAuction import settings
from Item.models import *
from Guser.models import GUser
import asyncio
from channels.db import database_sync_to_async
import json


class LiveBiddingConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        self.product_id = self.scope['url_route']['kwargs']['p_id']

        await self.send({
            "type": "websocket.accept"
        })

        await self.channel_layer.group_add(
            self.product_id,
            self.channel_name
        )

    async def websocket_receive(self, event):
        print("receive",  event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            bid = loaded_dict_data.get('bid')
            user_obj = self.scope['user']
            print(user_obj)
            p_id = self.product_id
            print(p_id)
            higest_bid,won,lesser_current,base=await self.update_bid(p_id, bid, user_obj)
            response = {
                'bid': higest_bid,
                'completed': won,
                'lesser_current':lesser_current,
                'base':base
            }
            if lesser_current or base:
                print("lesser base")
                await self.chat_message(
                    {
                        'type': 'chat_message',
                        'text': json.dumps(response)
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.product_id,
                    {
                        'type': 'chat_message',
                        'text': json.dumps(response)
                    }
                )

    async def websocket_disconnect(self, event):
        print("disconnected", event)



    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text'],

        })

    @database_sync_to_async
    def update_bid(self, p_id, bid, user_obj):
        product = Item.objects.get(id=p_id)
        guser=GUser.objects.get(user=user_obj)

        if product.G_user.user == user_obj:
            print("this user")
            return None
        else:
            print("new bid")

            if int(bid) >= product.base_price:
                print("not buying price")
                if int(bid) >= product.buying_price:
                    print("buying price")
                    bidding = bid_item.objects.create(item=product, bidUser=guser, bid_price=bid, status="Won")
                    product.status = "Completed"
                    product.save()

                    return bid, True, False, False
                if Item.get_bid_higest(product):
                    print("has a bid")
                    higest_bid=Item.get_bid_higest(product)
                    if int(bid) >= higest_bid.bid_price+higest_bid.bid_price*0.10:
                        bidding = bid_item.objects.create(item=product, bidUser=guser, bid_price=bid)

                        return bid, False, False,False
                    elif int(bid) < higest_bid.bid_price+higest_bid.bid_price*0.10:
                        print("less than current")
                        return bid,False, True, False
                else:
                    print("not has a bid")
                    bidding = bid_item.objects.create(item=product, bidUser=guser, bid_price=bid)

                    return bid, False, False, False
            else:
                print("less than bid price")
                return bid,False,False,True
