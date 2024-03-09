import flask
# Согласно архитектуре REST, обмен данными между клиентом и сервером осуществляется в формате JSON (реже — XML).
# Поэтому формат ответа сервера flask изменён с помощью метода jsonify, который преобразует наши данные в JSON.
from flask import request, jsonify

from . import db_session
from .news import News

# Механизм разделения приложения Flask на независимые модули
# Как правило, blueprint — логически выделяемый набор обработчиков адресов.
# Blueprint работает аналогично объекту приложения Flask, но в действительности он не является приложением.
blueprint = flask.Blueprint('news_api', __name__, template_folder='templates')


@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    # Можно явно указать, какие именно поля оставить в получившемся словаре.
    return jsonify(
        {'news': [item.to_dict(only=('title', 'content', 'user.name')) for item in news]})


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    # Согласно REST, далее нужно реализовать получение информации об одной новости. Фактически, мы уже получили из списка
    # всю информацию о каждой новости. При проектировании приложений по архитектуре REST обычно поступают таким образом:
    # когда возвращается список объектов, он содержит только краткую информацию (например, только id и заголовок)...
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    # ...а полную информацию (текст и автора) можно посмотреть с помощью запроса, который мы обработаем далее.
    # Можно явно указать, какие именно поля оставить в получившемся словаре.
    return jsonify({'news': news.to_dict(only=('title', 'content', 'user_id', 'is_private'))})


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private', 'is_published']):
        return jsonify({'error': 'Bad request'})
    # Проверив, что запрос содержит все требуемые поля, мы заносим новую запись в базу данных.
    # request.json содержит тело запроса, с ним можно работать, как со словарем.
    db_sess = db_session.create_session()

    news = News(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private'],
        is_published=request.json['is_published']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})
