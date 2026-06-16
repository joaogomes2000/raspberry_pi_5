variable "postgres_container_name" {
  description = "Name of the PostgreSQL container"
  type        = string
  default     = "my-postgres-db"
}

variable "postgres_image" {
  description = "Docker image for PostgreSQL"
  type        = string
  default     = "postgres:15-alpine"
}

variable "postgres_volume_name" {
  description = "Docker volume name for PostgreSQL data"
  type        = string
  default     = "postgres_data"
}

variable "postgres_external_port" {
  description = "External port exposed by PostgreSQL"
  type        = number
  default     = 5432
}

variable "postgres_user" {
  description = "PostgreSQL user"
  type        = string
  default     = "myuser"
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
  default     = "mypassword123"
}

variable "postgres_db" {
  description = "PostgreSQL database name"
  type        = string
  default     = "mydatabase"
}
