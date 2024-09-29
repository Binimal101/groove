FROM node:14

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the entire app directory into the container
COPY . .

# Build the app for production
RUN npm run build

# Install 'serve' to serve the build folder
RUN npm install -g serve

# Expose the port (optional, Cloud Run sets the PORT environment variable)
EXPOSE 8080

# Serve the build folder on the port specified by the PORT environment variable
CMD ["sh", "-c", "serve -s build -l $PORT"]
