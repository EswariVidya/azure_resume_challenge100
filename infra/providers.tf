terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.56.0"
    }
     random = {
      source = "hashicorp/random"
      version = "3.7.2"
    }
    }
  }
   
provider azurerm {
    resource_provider_registrations = "none"
    features {}

    use_cli  = var.auth_mode == "cli"
    use_oidc = var.auth_mode == "oidc"

    # optional: if you pass these, they'll be used; otherwise az CLI(env var) / OIDC context supplies them
    subscription_id = "621e31bb-64ce-4f5d-9120-88dd54acbc92"
}
provider "random" {
  # Configuration options
}