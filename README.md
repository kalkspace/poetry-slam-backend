# poetry-slam-backend

## Install

```
pipenv Install
```

## Running

```
pipenv run -- flask run --host 0.0.0.0
```

Posting a plain text file
```
curl -vl localhost:5000 --data-binary @training-data.txt -H "Content-Type: text/plain"
```