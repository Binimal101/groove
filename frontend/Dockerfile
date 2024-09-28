FROM node:14

# Set the working directory
WORKDIR /app

# Copy the package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the entire app directory into the container
COPY . .

# Build the app for production
RUN npm run build

# Use serve to serve the build folder
RUN npm install -g serve

# Serve the build folder on port 3000
CMD ["serve", "-s", "build", "-l", "3000"]

EXPOSE 3000
