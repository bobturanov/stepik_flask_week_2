import itertools

from flask import Flask, render_template
from data import title, subtitle, description, departures, tours

app = Flask(__name__)


@app.route('/')
def main():
    print(tours)
    return render_template('index.html', title=title, subtitle=subtitle, description=description, departures=departures,
                           tours=dict(itertools.islice(tours.items(), 6)))


@app.route('/departures/<departure_id>')
def render_departures(departure_id):
    departure_tours = {}
    for key, val in tours.items():
        if val['departure'] == departure_id:
            departure_tours.update({key: val})

    min_price_key = min(departure_tours.keys(), key=(lambda k: departure_tours[k]['price']))
    max_price_key = max(departure_tours.keys(), key=(lambda k: departure_tours[k]['price']))
    min_nights_key = min(departure_tours.keys(), key=(lambda k: departure_tours[k]['nights']))
    max_nights_key = max(departure_tours.keys(), key=(lambda k: departure_tours[k]['nights']))
    tours_info = {
        'min_price': departure_tours[min_price_key]['price'],
        'max_price': departure_tours[max_price_key]['price'],
        'min_nights': departure_tours[min_nights_key]['nights'],
        'max_nights': departure_tours[max_nights_key]['nights'],
    }

    return render_template('departure.html', title=title, subtitle=subtitle, description=description,
                           departures=departures, departure_id=departure_id, tours=departure_tours,
                           tours_info=tours_info)


@app.route('/tours/<num_id>')
def render_tours(num_id):
    tour = tours[int(num_id)]
    stars = '★' * int(tour['stars'])
    departure = departures[tour['departure']]
    return render_template("tour.html", title=title, departure=departure, tour=tour, departures=departures,
                           stars=stars)


@app.errorhandler(404)
def render_not_found(error):
    print(error)
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"


@app.errorhandler(500)
def render_server_error(error):
    return "Что-то не так, но мы все починим:\n{}".format(error.original_exception), 500


app.run()  # запустим сервер
