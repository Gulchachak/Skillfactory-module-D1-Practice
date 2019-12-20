import sys
import requests  
  
# Данные авторизации в API Trello  
base_url = "https://api.trello.com/1/{}" 
auth_params = {
    'key': "6d425cc0a565983e234e0daa1eb24e8a",    
    'token': "cc455ceda00bbd0ad99d75f471dbaf87240cf6373e152a44e8256b258dac2a13", }  
# board_id = "pliMmoaC"  
board_id = "5dfc3d70971ccf36f69c07cb"

def read():
    
    # response = requests.get(base_url.format('boards/' + board_id), params=auth_params).json()
    # print(response)
    
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()  
  
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:  
    for column in column_data:
        # Получим данные всех задач в колонке. Мы и раньше делали это, но до этого мы только перебирали элементы этих данных, 
        # А теперь мы ещё получим общее количество задач при помощи встроенной функции `len()`:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()  
        print(column['name'] + " - ({})".format(len(task_data)))  
  
        if not task_data:  
            print('\t' + 'Нет задач!')  
            continue  
        for task in task_data:  
            print('\t' + task['name'] + '\t' + task['id'])  

def create_column(column_name):  
    return requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id, **auth_params}).json()

def column_check(column_name):  
    column_id = None  
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()  
    for column in column_data:  
        if column['name'] == column_name:  
            column_id = column['id']  
            return column_id

def create(name, column_name):  
    column_id = column_check(column_name)  
    if column_id is None:  
        column_id = create_column(column_name)['id']  
  
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})
       

def move(name, column_name):  
    # Получим данные всех колонок на доске  
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()  
  
    # Среди всех колонок нужно найти задачу по имени и получить её id  
    task_id = None  
    for column in column_data:  
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()  
        for task in column_tasks:  
            if task['name'] == name:  
                task_id = task['id']  
                break  
        if task_id:  
            break  
  
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить,  
    # Получим ID колонки, в которую мы будем перемещать задачу  column_id = column_check(column_name)  
    if column_id is None:  
        column_id = create_column(column_name)['id']  
    # И совершим перемещение:  
    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})
          

if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3]) 
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
  