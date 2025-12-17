
output "site_url" {
    description = "The endpoint URL for web storage in the primary location. "
    value = azurerm_storage_account.azresumechallenge_st.primary_web_endpoint
}

output "rg_name" {
  value = azurerm_resource_group.azresumechallenge_rg.name
}

output "swb_name"{
    value = azurerm_storage_account.azresumechallenge_st.name
}

output "function_app_name" {
  value = azurerm_linux_function_app.func.name
}

output "function_default_hostname" {
  value = azurerm_linux_function_app.func.default_hostname
}

# output "cosmos_primary_sql_connection_string" {
#   value     = azurerm_cosmosdb_account.azresumechallenge_cosmos.primary_sql_connection_string
#   sensitive = true
# }

# # TXT records per custom domain: name + token (useful for Cloudflare)
# output "custom_domains_txt_records" {
#   value = {
#     for d, r in azurerm_static_web_app_custom_domain.domains :
#     d => {
#       name  = "_dnsauth.${d}"
#       value = r.validation_token
#     }
#   }
#   sensitive = true
# }