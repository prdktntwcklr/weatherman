# main.tf

terraform {
  required_providers {
    render = {
      source  = "registry.terraform.io/render-oss/render"
      version = "~> 1.0" # Use the latest version
    }
  }
}

provider "render" {
  # api_key and owner_id are often set via RENDER_API_KEY and RENDER_OWNER_ID environment variables
}

resource "render_web_service" "web" {
  name    = "weatherman-tf"
  plan    = "starter"
  region  = "singapore"
  start_command = "gunicorn \"weatherman:create_app()\""
  
  runtime_source = {
    native_runtime = {
      auto_deploy = true
      branch      = "main"
      build_command = "pip install -r requirements.txt"
      repo_url = "https://github.com/prdktntwcklr/weatherman"
      runtime  = "python"
    }
  }
}
