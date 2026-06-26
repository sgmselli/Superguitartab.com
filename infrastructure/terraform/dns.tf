# resource "azurerm_dns_zone" "main" {
#   name                = "superguitartab.com"
#   resource_group_name = azurerm_resource_group.main.name
# }

# resource "azurerm_dns_a_record" "root" {
#   name                = "@"
#   zone_name           = azurerm_dns_zone.main.name
#   resource_group_name = azurerm_resource_group.main.name
#   ttl                 = 300

#   records = [
#     azurerm_public_ip.app.ip_address
#   ]
# }

# resource "azurerm_dns_cname_record" "www" {
#   name                = "www"
#   zone_name           = azurerm_dns_zone.main.name
#   resource_group_name = azurerm_resource_group.main.name
#   ttl                 = 43200

#   record = "superguitartab.com"
# }

# resource "azurerm_dns_cname_record" "brevo1" {
#   name                = "brevo1._domainkey"
#   zone_name           = azurerm_dns_zone.main.name
#   resource_group_name = azurerm_resource_group.main.name
#   ttl                 = 43200

#   record = "b1.superguitartab-com.dkim.brevo.com"
# }

# resource "azurerm_dns_cname_record" "brevo2" {
#   name                = "brevo2._domainkey"
#   zone_name           = azurerm_dns_zone.main.name
#   resource_group_name = azurerm_resource_group.main.name
#   ttl                 = 43200

#   record = "b2.superguitartab-com.dkim.brevo.com"
# }

# resource "azurerm_dns_txt_record" "brevo_code" {
#   name                = "@"
#   zone_name           = azurerm_dns_zone.main.name
#   resource_group_name = azurerm_resource_group.main.name
#   ttl                 = 300

#   record {
#     value = "brevo-code:c7786dea4e26dc591d247ead370be74f"
#   }
# }

# resource "azurerm_dns_txt_record" "spf" {
#   name                = "@"
#   zone_name           = azurerm_dns_zone.main.name
#   resource_group_name = azurerm_resource_group.main.name
#   ttl                 = 300

#   record {
#     value = "v=spf1 include:spf.privateemail.com ~all"
#   }
# }

# resource "azurerm_dns_txt_record" "dmarc" {
#   name                = "_dmarc"
#   zone_name           = azurerm_dns_zone.main.name
#   resource_group_name = azurerm_resource_group.main.name
#   ttl                 = 3600

#   record {
#     value = "v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com"
#   }
# }

# resource "azurerm_dns_mx_record" "mx" {
#   name                = "@"
#   zone_name           = azurerm_dns_zone.main.name
#   resource_group_name = azurerm_resource_group.main.name
#   ttl                 = 14400

#   record {
#     preference = 10
#     exchange   = "mx1.privateemail.com"
#   }

#   record {
#     preference = 10
#     exchange   = "mx2.privateemail.com"
#   }
# }