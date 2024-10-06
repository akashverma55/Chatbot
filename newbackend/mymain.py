from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import mydb
import mygenric

app = FastAPI()

Inprogress_Order={
   
}

@app.post("/webhook")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    # if intent == "track.order":
    #     response=track_order(parameters)
    #     return response
    
    # if intent == "order.add":
    #     response=add_order(parameters)
    #     return response
    session_ID=mygenric.extract_session_id(output_contexts[0]['name'])
    intent_handler_dict = {
        'order.add': add_order,
        'OrderRemove':remove_order,
        'OrderComplete': complete_order,
        'track.order': track_order
    }

    return intent_handler_dict[intent](parameters, session_ID)

    
        
def add_order(parameters:dict,session_ID: str):
    food_items=parameters["Food-Items"]
    quantity=parameters["number"]

    if len(food_items)!=len(quantity):
        fulfillment_text="can you please specify the correct quantity of your order"
    else:
        new_food_dict=dict(zip(food_items,quantity))
        if session_ID in Inprogress_Order:
            # merging if session_id is present
            current_food_dict=Inprogress_Order[session_ID]
            current_food_dict.update(new_food_dict)
            Inprogress_Order[session_ID]=current_food_dict
        else:
            Inprogress_Order[session_ID]=new_food_dict
        order_str=mygenric.get_string_of_food_dict(Inprogress_Order[session_ID])

        fulfillment_text=f"So far you have : {order_str}. Want to add anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def remove_order(parameters: dict,session_ID):
    if session_ID in Inprogress_Order:
        current_order=Inprogress_Order[session_ID]
        food_items=parameters["food-items"]

        removed_items=[]
        no_such_items=[]
        for item in food_items:
            if item not in current_order:
                no_such_items.append(item)
            else:
                removed_items.append(item)
                del current_order[item]

        if len(removed_items)>0:
            fulfillment_text=f"Removed {", ".join(removed_items)}from your order"
        else:
            fulfillment_text="having problem from removed items"

        if len(no_such_items)>0:
            fulfillment_text=f"Your current order does not have {", ".join(no_such_items)}"
        else:
            fulfillment_text="having problem from no such items"
        
        if len(current_order.keys())==0:
            fulfillment_text="Your order is empty."
        else:
            order_str=mygenric.get_string_of_food_dict(current_order)
            fulfillment_text=f"Here what is left in your order: {order_str}"

        return JSONResponse(content={
            "fulfillment_text": fulfillment_text
        })

    else:
        return JSONResponse(content={
            "fulfillmentText":"Sorry, I'm having a trouble finding your order. Can you please order it again"
        })


def complete_order(parameters: dict,session_ID):
    if session_ID in Inprogress_Order:
        order = Inprogress_Order[session_ID]
        print(order)
        order_id=save_to_DB(order)

        if order_id == -1:
            fulfillment_text= "Sorry! I am having trouble finding your order can you please place your order again."
        else:
            order_total=mydb.get_total(order_id)
            fulfillment_text=f"Awesome, we have placed your order."\
                            f"Here is your order ID # {order_id}."\
                            f"Your total is {order_total}."
    else:
        fulfillment_text= "Sorry! I am having trouble finding your order can you please place your order again."

    del Inprogress_Order[session_ID]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def save_to_DB(order: dict):
    # order = {"pizza":2, "chole": 1}

    new_order_id=mydb.get_new_order_id()

    for food_item, quantity in order.items():
        for food_item, quantity in order.items():
            rcode=mydb.insert_order_item(
            food_item,
            quantity,
            new_order_id
            )

            if rcode==-1:
                return -1
            
        mydb.insert_status(new_order_id, "In Progress")
        
        return new_order_id

def track_order(parameters: dict, session_ID: str):
    order_ID=int(parameters['number-integer'])
    
    order_Status=mydb.get_order_status(order_ID)

    if order_Status:
        fulfillment_text= f"The order status for order id: {order_ID} is: {order_Status}"
    else:
        fulfillment_text=f"NO order found with order id: {order_ID}"
    # Return a JSON response for the "TakingTrackOrder" intent
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


@app.get("/")
async def read_root():
    return {"message": "Hello, World"}
