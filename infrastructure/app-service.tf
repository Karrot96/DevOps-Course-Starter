resource "azurerm_app_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name                = "AlexKApp-${random_string.random_identifier.result}"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|karrot96/todo-app:latest"
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGODB_CONNECTION_STRING"  = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase"
    "APP_NAME"                   = "appName=@${azurerm_cosmosdb_account.main.name}@"
    "CLIENT_ID"                  = var.client_id
    "CLIENT_SECRET"              = var.client_secret
    "DOCKER_ENABLE_CI"           = true
    "FLASK_APP"                  = "app"
    "FLASK_ENV"                  = "production"
    "SECRET_KEY"                 = var.secret_key
    "WRITER_ID"                  = var.writer_id
    "LOGGLY_TOKEN"               = var.loggly_token
    "LOG_LEVEL"                  = var.log_level
  }
}
