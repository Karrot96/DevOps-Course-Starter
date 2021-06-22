terraform {
  backend "azurerm" {
    resource_group_name  = "SoftwirePilot_AlexKaret_ProjectExercise"
    storage_account_name = "tstate5718"
    container_name       = "tstate"
    key                  = "terraform.tfstate"
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "random" {
  # Configuration options
}

resource "random_string" "random_identifier" {
  length  = 8
  special = false
}

data "azurerm_resource_group" "main" {
  name     = var.resource_group_name
}
