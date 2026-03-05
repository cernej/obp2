from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .models import Rate, db

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        codes = db.session.query(Rate.code).distinct().all()
        codes = [code[0] for code in codes]
        return render_template('index.html', codes=codes)

    @app.route('/update', methods=['POST'])
    def update():
        from .cnb import fetch_exchange_rates
        date, rates = fetch_exchange_rates()
        for code, (amount, rate) in rates.items():
            existing_rate = Rate.query.filter_by(date=str(date), code=code).first()
            if existing_rate:
                existing_rate.amount = amount
                existing_rate.rate = rate
            else:
                new_rate = Rate(date=str(date), code=code, amount=amount, rate=rate)
                db.session.add(new_rate)
        db.session.commit()
        return f'Exchange rates updated for {date}'

    @app.route('/code/<code>')
    def code_info(code):
        rates = db.session.query(Rate).filter_by(code=code).order_by(Rate.date).all()
        if not rates:
            return f'No exchange rates found for code: {code}'
        response = f'Exchange rates for {code}:\n'
        for rate in rates:
            response += f'<br>{rate.date}: {rate.amount} {code} = {rate.rate:.4f} CZK'
        return render_template('currency.html', code=code, rates=rates)

    @app.route('/api/rates/<code>')
    def api_rates(code):
        rates = db.session.query(Rate).filter_by(code=code).order_by(Rate.date).all()
        if not rates:
            return {'error': f'No exchange rates found for code: {code}'}, 404
        data = [{'date': rate.date, 'czk_per_1': rate.rate / rate.amount} for rate in rates]
        return {'code': code, 'data': data}

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)