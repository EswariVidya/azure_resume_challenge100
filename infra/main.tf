# ---------------- RG & helpers ----------------
resource "random_string" "resourcename_randomstring" {
    length = 7
    lower = true
    numeric = true
    special = false
    upper = false
    #override_special = "/$100"
}
##resource group

resource "azurerm_resource_group" "azresumechallenge_rg" {
  name     = "azresumechallenge_rg${random_string.resourcename_randomstring.result}"
  location = var.location
}

# ---------------- Storage account ----------------
resource "azurerm_storage_account" "azresumechallenge_st" {
  name                     = "azrcst${random_string.resourcename_randomstring.result}"
  resource_group_name      = azurerm_resource_group.azresumechallenge_rg.name
  location                 = azurerm_resource_group.azresumechallenge_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
}

# ---------------- Static Website (Storage account) ----------------
resource "azurerm_storage_account_static_website" "azresumechallenge_stweb" {
    storage_account_id = azurerm_storage_account.azresumechallenge_st.id
    index_document     = "index.html"
    error_404_document = "404.html"
  
}
# locals {
#   site_files = fileset("/Users/vidya/Desktop/Vidya folder/azure_resume_challenge100/frontend", "**")
# }

# #Frontend files upload must be replaced to upload files from Github Actions pipeline/Azcopy sync
# resource "azurerm_storage_blob" "azresumechallenge_stblob" {
#   for_each               = local.site_files
#   name                   = each.value
#   storage_account_name   = azurerm_storage_account.azresumechallenge_st.name
#   storage_container_name = "$web"
#   type                   = "Block"
#   source                 = "/Users/vidya/Desktop/Vidya folder/azure_resume_challenge100/frontend/${each.value}"
#   content_type           = lookup({
#     html = "text/html"
#     css  = "text/css"
#     js   = "application/javascript"
#     png  = "image/png"
#     svg  = "image/svg+xml"
#   }, regex("\\.([^.]+)$", each.value)[0], "application/octet-stream")
# }

##Backend resources


# ---------------- Cosmos DB (SQL) ----------------
resource "azurerm_cosmosdb_account" "azresumechallenge_cosmos" {
  name                = "azrccdb${random_string.resourcename_randomstring.result}"
  location            = azurerm_resource_group.azresumechallenge_rg.location
  resource_group_name = azurerm_resource_group.azresumechallenge_rg.name

  offer_type          = "Standard"

  kind                = "GlobalDocumentDB"
  free_tier_enabled   = true

  consistency_policy {
    consistency_level = "Session"
  }

  # Serverless capability (mutually exclusive with Free Tier)
  # dynamic "capabilities" {
  #   for_each = var.cosmos_serverless ? [1] : []
  #   content {
  #     name = "EnableServerless"
  #   }
  # }

  geo_location {
    location          = "West US 2"
    failover_priority = 0
  }

  # lifecycle {
  #   precondition {
  #     condition     = !(var.cosmos_serverless && var.cosmos_free_tier)
  #     error_message = "Cosmos Serverless and Free Tier cannot both be true."
  #   }
  # }
}

resource "azurerm_cosmosdb_sql_database" "db" {
  name                = "azureresumecounter"
  resource_group_name = azurerm_resource_group.azresumechallenge_rg.name
  account_name        = azurerm_cosmosdb_account.azresumechallenge_cosmos.name
  # When serverless: do NOT set throughput / autoscale
}

resource "azurerm_cosmosdb_sql_container" "container" {
  name                  = "counter"
  resource_group_name   = azurerm_resource_group.azresumechallenge_rg.name
  account_name          = azurerm_cosmosdb_account.azresumechallenge_cosmos.name
  database_name         = azurerm_cosmosdb_sql_database.db.name
  partition_key_paths   = ["/id"] # v4 expects a LIST
  partition_key_version = 2
}

# ---------------- Function App (Linux, Consumption Y1) ----------------
resource "azurerm_storage_account" "func_sa" {
  name                     = "azrcfst${random_string.resourcename_randomstring.result}"
  resource_group_name      = azurerm_resource_group.azresumechallenge_rg.name
  location                 = var.func_location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  allow_nested_items_to_be_public = false
}

resource "azurerm_service_plan" "plan" {
  name                = "ASP-azrc-${random_string.resourcename_randomstring.result}"
  resource_group_name = azurerm_resource_group.azresumechallenge_rg.name
  location            = var.func_location
  os_type             = "Linux"
  sku_name            = "Y1"         # Consumption
  # tags                = local.tags
}

resource "azurerm_linux_function_app" "func" {
  name                       = "azrcfa-${random_string.resourcename_randomstring.result}"
  resource_group_name        = azurerm_resource_group.azresumechallenge_rg.name
  location                   = var.func_location
  service_plan_id            = azurerm_service_plan.plan.id
  storage_account_name       = azurerm_storage_account.func_sa.name
  storage_account_access_key = azurerm_storage_account.func_sa.primary_access_key
  https_only                 = true
  functions_extension_version = "~4"
  # tags                        = local.tags

  site_config {
    application_stack {
      python_version = var.python_version
    }
  }

  app_settings = {
    "CosmosDbConnectionString" = azurerm_cosmosdb_account.azresumechallenge_cosmos.primary_sql_connection_string
    "COSMOS_DATABASE"             = azurerm_cosmosdb_sql_database.db.name
    "COSMOS_CONTAINER"          = azurerm_cosmosdb_sql_container.container.name
    "COSMOS_ENDPOINT" = azurerm_cosmosdb_account.azresumechallenge_cosmos.endpoint
    "COSMOS_KEY" = azurerm_cosmosdb_account.azresumechallenge_cosmos.primary_key
    # add your own runtime vars here (e.g., COUNTER_ID)
  }
}