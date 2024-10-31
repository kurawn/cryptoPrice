### Build the Docker Image
```bash
docker build -t crypto-price-app .
```
### Run the Container
```bash
docker run -p 8000:8000 crypto-price-app
```
### Open the Application
After starting the container, open your web browser and go to: http://127.0.0.1:8000