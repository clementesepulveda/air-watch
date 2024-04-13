# Air Watch

Project made for the class IIC3103, Integration Workshop. Using mock data. You can check out the deployment at:

Frontend:
- [https://air-watch.vercel.app/insights]()

Backend:
- [https://air-watch-api.onrender.com/]()

## Frontend

Developed using SvelteKit, the frontend features comprehensive views for flights, allowing users to search by origin, destination, or both, and sort by any attribute. Additionally, it includes detailed views for specific flights, displaying trajectory and passenger information. Lastly, there's a view for insights presenting graphs for various data points.

Utilized various technologies such as Echarts for creating graphs and Leaflet for integrating maps.

### .env File
```
PUBLIC_BASE_URL="http://localhost:8000"
```

### Instalation
```
npm install
npm run dev
```
Go to `http://localhost:5173`.

## Backend

Built with FastAPI, the backend system handles data storage as files, optimizes them for improved usability, and provides an open endpoint for data retrieval.

Although originally designed to download flight data, this functionality has been deprecated. The process involved downloading raw data initially, followed by optimization to reduce processing time significantly. Fetching unprocessed data could take several seconds or even minutes, whereas optimized data retrieval typically took only seconds. The chosen optimization format was h5 due to its superior performance compared to other formats such as JSON, YAML, CSV, and XML, determined through experimentation.

### private_key.json

Used for downloading the data from Google Cloud. 

### Instalation

```
pip install -r requirements
python3 -m uvicorn main:app --reload
```
Go to `http://localhost:8000`.

## Github Actions

### call_download_endpoint.py

During the project's development, data updated occurred every few hours, necessitating frequent updates to project files. To mitigate potential delays for users accessing the website and needing all necessary files, pre-downloading was implemented.

### call_sleeping.py

When hosted on a free-tier platform like render.com, the service would enter a sleeping state to conserve resources, resulting in occasional cold starts. To maintain continuous functionality, this script would periodically call the URL to prevent service interruption.
