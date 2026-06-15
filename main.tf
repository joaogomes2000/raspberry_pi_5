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
  name = "postgres_data"
}

# Pull the official PostgreSQL image
resource "docker_image" "postgres" {
  name         = "postgres:15-alpine"
  keep_locally = false
}

# Run the PostgreSQL container
resource "docker_container" "postgres" {
  rm    = true
  image = docker_image.postgres.image_id
  name  = "my-postgres-db"


  # Configure environment variables for database credentials
  env = [
    "POSTGRES_USER=myuser",
    "POSTGRES_PASSWORD=mypassword123",
    "POSTGRES_DB=mydatabase"
  ]

  # Map the default Postgres port (5432) to your local machine
  ports {
    internal = 5432
    external = 5432
  }

  # Attach the volume to the container's default data directory
  volumes {
    volume_name    = docker_volume.pg_data.name
    container_path = "/var/lib/postgresql/data"
  }

}
