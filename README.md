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
- Update Git adding .gitignore file add local.settings.json 

##Deploy Azure Function App

- Deploy locally created Function App to Azure
  - Choose Create Azure Function app on Azure advanced option on VS Code
  - Choose/Create Resource Group, Storage Account, App Insights
  - Update Python Runtime Version in Azure Portal -> Function App -> Settings -> Configuration -> Stack Settings
  - Upload the settings locally so that function is deployed properly to Azure

![alt text](image.png)

## Deployed the Front end website (again) with the updated javascript 

- Update the CORS on Azure Functions app with primary endpoint(azure storage static website) so that the visitor count is visible.

## Azure CDN/FrontDoor deployment failed

- Free Trial and Student account is forbidden for Azure Frontdoor resources.

## CI/CD - Github workflows
- Create .github folder and create workflows for frontend and backend yml files.
- Generate the deployment credentials by running the following command.
  ```bash
  az ad sp create-for-rbac --name {myStaticSite} --role contributor --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} --sdk-auth
  ```
- JSON output will have the credentials and paste them to Github->Settings->Security (Secrets and variables)->New secret