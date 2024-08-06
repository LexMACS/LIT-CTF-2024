# Use the official Node.js image as the base image
FROM node:16

# Set the working directory inside the container
WORKDIR /app

# Install Bun
RUN curl -fsSL https://bun.sh/install | bash

# Add Bun to PATH
ENV BUN_INSTALL=/root/.bun
ENV PATH=$BUN_INSTALL/bin:$PATH

# Copy package.json and bun.lockb to the working directory
COPY package.json bun.lockb ./

# Install project dependencies using Bun
RUN bun install

# Copy the rest of the application code to the working directory
COPY . .

# Build the TypeScript project
#RUN bun run build

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["bun", "run", "dev"]
