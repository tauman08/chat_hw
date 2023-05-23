import json


def write_order_to_json(item,quantity,price,buyer,date):
    dict_param = {
        'item':item,
        'quantity':quantity,
        'price':price,
        'buyer':buyer,
        'date':date
        }
    with open('orders.json','w') as f:
        json.dump(dict_param, f, indent=4)

    

if __name__ == '__main__':
    write_order_to_json('Паровоз',5,10000020,'Пупкин','21.01.2023')