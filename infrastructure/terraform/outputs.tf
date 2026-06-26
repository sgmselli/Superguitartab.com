output "vm_app_public_ip" {
  description = "Public IP address of the app virtual machine"
  value       = azurerm_public_ip.app.ip_address
}
