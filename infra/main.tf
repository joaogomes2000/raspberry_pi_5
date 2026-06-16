terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.0"
    }
  }
}

provider "docker" {}

# Create a persistent volume so your data isn't lost when the container stops
resource "docker_volume" "pg_data" {
  name = var.postgres_volume_name
}

# Pull the official PostgreSQL image
resource "docker_image" "postgres" {
  name         = var.postgres_image
  keep_locally = false
}

# Run the PostgreSQL container
resource "docker_container" "postgres" {
  image = docker_image.postgres.image_id
<<<<<<< Updated upstream:main.tf
  name  = "my-postgres-db"
  restart = "always"
=======
  name  = var.postgres_container_name

>>>>>>> Stashed changes:infra/main.tf

  # Configure environment variables for database credentials
  env = [
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}"
  ]

  # Map the default Postgres port (5432) to your local machine
  ports {
    internal = 5432
    external = var.postgres_external_port
  }

  # Attach the volume to the container's default data directory
  volumes {
    volume_name    = docker_volume.pg_data.name
    container_path = "/var/lib/postgresql/data"
  }

  lifecycle {
    create_before_destroy = true
  }

}
