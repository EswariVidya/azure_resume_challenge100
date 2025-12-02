# vidya azureresume
My own cloud resume

## First steps

- Frontend folder contains the website.
- viewCount.js file contains the visitor counter code.

## Created backend 
- Azure Cosmos DB on Azure with Container to store count value.
- Setup Azure Function app locally 
- Install Azure Functions Core Tools 
- Run below command 
```bash
npm i -g azure-functions-core-tools@4 --unsafe-perm true
```

- To start azure functions locally

```bash
func host start
```

- To bind Cosmos DB Azure Functions app python
  - add to requirements.txt 
  - run pip install to install requirements
```bash
pip install -r requirements.txt
``` 
  - Update local.settings.json file with Cosmos DB credentials (kept secret)