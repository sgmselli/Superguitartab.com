variable "ssh_public_key" {
  description = "SSH public key for VM access"
  type        = string
  sensitive   = true
}

variable "location" {
  type    = string
  default = "westeurope"
}

variable "resource_group_name" {
  type    = string
  default = "rg-superguitartab-prod-westeurope"
}

variable "container_registry_name" {
  type    = string
  default = "superguitartab"
}

variable "vnet_name" {
  type    = string
  default = "vnet-superguitartab-prod-westeurope"
}

variable "subnet_app_name" {
  description = "Subnet for the virtual machine containing the main app"
  type        = string
  default     = "subnet-superguitartab-prod-main-westeurope"
}

variable "subnet_db_name" {
  description = "Subnet for the virtual machine containing the relational database"
  type        = string
  default     = "subnet-superguitartab-prod-db-westeurope"
}

variable "nsg_app_name" {
  description = "Network Security Group for the main app's subnet"
  type        = string
  default     = "nsg-superguitartab-prod-main-westeurope"
}

variable "nsg_db_name" {
  description = "Network Security Group for the relational database's subnet"
  type        = string
  default     = "nsg-superguitartab-prod-db-westeurope"
}

variable "vm_app_name" {
  description = "Virtual machine containing the containerised app"
  type        = string
  default     = "vm-superguitartab-prod-main-westeurope"
}

variable "vm_app_size" {
  description = "Size of our app's virtual machine"
  type        = string
  default     = "Standard_B2ts_v2"
}

variable "admin_username" {
  description = "Username used to access virtual machine"
  type        = string
  default     = "mattsellings"
}

variable "db_name" {
  type        = string
  default     = "superguitartabdb"
}

variable "db_size" {
  type        = string
  default     = "B_Standard_B1ms"
}

variable "db_storage_size_mb" {
  type        = number
  default     = 32768
}

variable "db_backup_retention_days" {
  type        = number
  default     = 7
}

variable "db_admin_username" {
  type = string
}

variable "db_firewall_name" {
  type        = string
  default     = "allow-vm-access"
}

variable "db_admin_password" {
  type      = string
  sensitive = true
}