output "vm_app_public_ip" {
  description = "Public IP address of the app virtual machine"
  value       = azurerm_public_ip.app.ip_address
}

output "acr_username" {
  value = azurerm_container_registry.main.admin_username
}

output "acr_password" {
  value     = azurerm_container_registry.main.admin_password
  sensitive = true
}
