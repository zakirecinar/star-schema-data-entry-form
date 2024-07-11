from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=5001)  # 5000 de hata aldığım için 5001 kullandığımı belirttim
