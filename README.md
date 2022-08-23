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
jq -Rns inputs diemade.txt | curl -vl localhost:5000 -d@- -H "Content-Type: application/json"
```