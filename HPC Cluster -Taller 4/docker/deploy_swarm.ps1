# Build the image
docker build -t travel-calculator:1.0 .

# Initialize Swarm if not already active (ignore error if already part of swarm)
try {
    docker swarm init
}
catch {
    Write-Host "Swarm already initialized or node is already part of a swarm."
}

# Remove existing service if it exists to ensure fresh deploy
docker service rm calculator

# Create the service with 4 replicas
# Mapping port 5000 to 5000
docker service create --name calculator --replicas 4 -p 5000:5000 travel-calculator:1.0

# Verify service
docker service ls
docker service ps calculator
