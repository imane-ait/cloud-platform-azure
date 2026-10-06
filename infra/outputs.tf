output "app_public_ip" {
  description = "Adresse IP publique de la machine de l'appli"
  value       = azurerm_public_ip.app.ip_address
}