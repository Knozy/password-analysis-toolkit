from app import create_app, db
import logging

app = create_app('development')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    app.run(
       host='0.0.0.0',
       port=5000, debug=True
    )
