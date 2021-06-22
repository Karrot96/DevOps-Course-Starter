variable "resource_group_name" {
  default = "SoftwirePilot_AlexKaret_ProjectExercise"
}

variable "location" {
  default = "uksouth"
}

variable "cosmos_account_name" {
  default = "alex-k"
}

variable "cosmos_db_name" {
  default = "todo-app"
}

variable "client_id" {
  sensitive = true
}

variable "client_secret" {
  sensitive = true
}

variable "secret_key" {
  sensitive = true
}

variable "writer_id" {
  sensitive = true
}

variable "loggly_token" {
  sensitive = true
}

variable "log_level" {
  default = "INFO"
}
