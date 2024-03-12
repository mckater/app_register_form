from requests import get, post, delete

print(get('http://localhost:5000/api/v2/news').json())
# print(get('http://localhost:5000/api/v2/news/4').json())
# print(get('http://localhost:5000/api/v2/news/52').json())  # нет такой новости
# print(get('http://localhost:5000/api/v2/news/q').json())  # не число

# print(post('http://localhost:5000/api/v2/news').json())  # нет словаря
# print(post('http://localhost:5000/api/v2/news', json={'title': 'Sonya'}).json())  # не все поля
# print(post('http://localhost:5000/api/v2/news', json={'title': 'Flask-RESTful',
#                                                       'content': 'Создадим вторую версию нашего REST-сервиса.',
#                                                       'is_private': False, 'is_published': True, 'user_id': 1}).json())
#
# print(delete('http://localhost:5000/api/v2/news/999').json())  # id = 999 нет в базе
# print(delete('http://localhost:5000/api/v2/news/4').json())
