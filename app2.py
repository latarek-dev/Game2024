from flask import Flask, render_template_string, url_for, redirect, request

app = Flask(__name__)

@app.before_request
def redirect_to_home():
    # Używamy request.endpoint, aby sprawdzić, czy użytkownik nie jest na stronie głównej
    if request.endpoint != 'home' and request.endpoint != 'static':
        return redirect(url_for('home'))

@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interaktywna gra miejska</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f9f9f9;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #333;
                padding-top: 50px;
            }
            h1 {
                margin-bottom: 30px;
                font-size: 2.5em;
                font-weight: bold;
                color: #0056b3;
            }
            p {
                font-size: 1.1em;
                line-height: 1.8;
                margin-bottom: 20px;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .btn-primary {
                background-color: #0056b3;
                border-color: #0056b3;
            }
            .btn-primary:hover {
                background-color: #004494;
                border-color: #004494;
            }
            .content {
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            img {
                display: block;
                margin: 20px auto;
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <div class="container content">
            <h1 class="text-center">Zaproszenie na interaktywną grę miejską</h1>
            <p>Zapraszamy harcerzy od 15 r.ż. do zagrania w interaktywną grę miejską "Chcieliśmy być wolni - kadry z Powstania". Gra prowadzi przez ulice i place Śródmieścia Północnego śladem legendarnego powstańczego fotografa - Eugeniusza Lokajskiego ps. "Brok". Zagadki, łamigłówki, szybkość i orientacja w terenie.</p>
            <p class="text-center"><a href="https://www.facebook.com/events/496807759701473/?ref=newsfeed" class="btn btn-primary">Zobacz wydarzenie na Facebooku</a></p>
            <p>Aby zagrać, należy ze strony <a href="https://www.1944.pl/artykul/gra-miejska-chcielismy-byc-wolni,5510.html">Muzeum Powstania Warszawskiego</a> pobrać specjalną aplikację i zeskanować kod QR. Zapraszamy do gry!</p>
            <img src="{{ url_for('static', filename='images/gra_terenowa.jpg') }}" alt="Zdjęcie związane z grą miejską">
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run()
