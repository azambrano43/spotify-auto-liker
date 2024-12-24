from app import create_app

app = create_app()

if __name__ == '__main__':
    #app = create_app()
    # Imprime todas las rutas disponibles
    with app.app_context():
        print(app.url_map)
    app.run(debug=True)