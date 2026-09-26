terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "sttfstateimane01"
    container_name       = "tfstate"
    key                  = "cloud-platform.tfstate"
  }
}