import yaml

def write_to_yaml():
    lst = ['one','two','three']
    dict_example = {
        'item_1':'163€',
        'item_2':'8381€',
        'item_3':'8364€'
        }

    date_to_yaml = {
        'key_1':lst,
        'key_2':1000,
        'key_3':dict_example}
    with open('example.yaml','w', encoding='utf-8') as f:
        yaml.dump(date_to_yaml,f,default_flow_style=False,allow_unicode=True)

    with open('example.yaml','r',encoding='utf-8') as f:
        print(yaml.load(f,Loader=yaml.SafeLoader))


if __name__ == '__main__':
    write_to_yaml()

