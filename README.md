# DockerOptimizerAPI


## Instructions To Run Locally (for macbook):
**Step 1** 

Create or Ask Mike for .env file

**Step 2**
```bash
python3 -m venv flaskenv \
source flaskenv/bin/activate \
pip install -r requirements.txt
```

**Step 3**

If running on docker make sure in app.py the host is set to 0.0.0.0
```bash
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```
in addition change the start script within docker to be the following:
```bash
COPY start.sh /start.sh
RUN chmod +x /start.sh
```

and
```bash
ENTRYPOINT ["/start.sh"]
```
and change this:
```bash
EXPOSE 5000
```
To run the container run the following command:
```bash
docker run -d --privileged --name my-docker-optimizer -p 5000:5000 --env-file .flaskenv mikeguyon98/my-docker-optimizer
```

If not running with docker, remove the host argument
```bash
if __name__ == '__main__':
    app.run(debug=True)
```
For deployment with docker:
```bash
if __name__ == '__main__':
    app.run(host='0.0.0.0')
```
in addition change the start script within dockerfile to be the following:
```bash
COPY productionstart.sh /productionstart.sh
RUN chmod +x /productionstart.sh
```

and
```bash
ENTRYPOINT ["/productionstart.sh"]
```

and change this:
```bash
EXPOSE 5000
```

To run the container run the following command:
```bash
docker run -d --privileged --name my-docker-optimizer-prod -p 5000:5000 --env-file .flaskenv mikeguyon98/my-docker-optimizer-prod
```

## API Inputs
- docker image name
- Dockerfile text
