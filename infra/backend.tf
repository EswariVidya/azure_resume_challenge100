terraform {
  backend "azurerm" {
    resource_group_name  = "azureresumechallengegroup"   
    storage_account_name = "azresumewebsite"
    container_name       = "tfstate"
    key                  = "cloudchallenge.tfstate" 
  }
}