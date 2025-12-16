##############################
# variables.tf
##############################

# Auth mode: "cli" for local (az login), "oidc" for GitHub Actions
variable "auth_mode" {
  type        = string
  default     = "cli"
  validation {
    condition     = contains(["cli", "oidc"], var.auth_mode)
    error_message = "auth_mode must be one of: cli, oidc"
  }
}

# Optional—leave null to use az CLI / OIDC context
variable "subscription_id" {
  type        = string
  default     = null
  description = "Azure subscription ID (optional when using CLI/OIDC)."
}
variable "tenant_id" {
  type        = string
  default     = null
  description = "Azure tenant ID (optional when using CLI/OIDC)."
}

#variable "site_url" {
 # type        = string
 # description = "Public site URL from storage account."
#}


# variable "name_prefix" {
#   description = "Prefix used in resource names (e.g., 'cloudchallenge')."
#   type        = string
# }

variable "location" {
  description = "Azure region for RG/Functions/Cosmos (e.g., 'North Europe')."
  type        = string
  default     = "North Europe"
}

variable "func_location" {
  description = "Azure region for RG/Functions/Cosmos (e.g., 'North Europe')."
  type        = string
  default     = "West Europe"
}


# ---------------- Cosmos DB ----------------

# variable "cosmos_free_tier" {
#   description = "Enable Cosmos DB Free Tier (cannot be true if cosmos_serverless is also true)."
#   type        = bool
#   default     = false
# }

# variable "cosmos_serverless" {
#   description = "Enable Cosmos DB Serverless (cannot be true if cosmos_free_tier is also true)."
#   type        = bool
#   default     = true
# }

# variable "cosmos_db_name" {
#   description = "Cosmos SQL database name."
#   type        = string
#   default     = "ClickCounter"
# }

# variable "cosmos_container" {
#   description = "Cosmos SQL container name."
#   type        = string
#   default     = "Counts"
# }

# variable "cosmos_partition" {
#   description = "Cosmos SQL partition key path."
#   type        = string
#   default     = "/id"
# }

# # ---------------- Function App ----------------

# variable "functions_language" {
#   description = "Function App language (this stack assumes Python unless you extend main.tf)."
#   type        = string
#   default     = "python"

#   validation {
#     condition     = var.functions_language == "python"
#     error_message = "Only 'python' is supported by the current main.tf site_config. Update main.tf if using another language."
#   }
# }

variable "python_version" {
  description = "Python runtime version for the Function App."
  type        = string
  default     = "3.11"
}

# ---------------- Static Web App ----------------

# variable "custom_domains" {
#   description = "Optional list of custom domains for the SWA (DNS TXT validation)."
#   type        = list(string)
#   default     = []
# }