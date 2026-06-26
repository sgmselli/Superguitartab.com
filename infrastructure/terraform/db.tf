resource "azurerm_postgresql_flexible_server" "db" {
  name                = var.db_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  version = "18"

  administrator_login    = var.db_admin_username
  administrator_password = var.db_admin_password

  storage_mb = var.db_storage_size_mb

  sku_name = var.db_size

  backup_retention_days = var.db_backup_retention_days

  public_network_access_enabled = true
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "vm" {
  name             = var.db_firewall_name
  server_id        = azurerm_postgresql_flexible_server.db.id
  start_ip_address = azurerm_public_ip.app.ip_address
  end_ip_address   = azurerm_public_ip.app.ip_address
}