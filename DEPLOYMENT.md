# Deploying Redis Clone API on Render

This guide will walk you through deploying your Redis Clone API on Render.com.

## Prerequisites

- A [Render](https://render.com) account
- Your project code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

### 1. Push Your Code to a Git Repository

Make sure your code is pushed to a Git repository (GitHub, GitLab, etc.) that Render can access.

### 2. Create a New Web Service on Render

1. Log in to your Render account
2. Click on the "New +" button and select "Blueprint" from the dropdown menu
3. Connect your Git repository
4. Render will automatically detect the `render.yaml` configuration file and set up your services

### 3. Configure Environment Variables (if needed)

The `render.yaml` file already configures the connection between your web service and Redis instance. However, if you need additional environment variables:

1. Go to your web service dashboard
2. Click on "Environment"
3. Add any additional environment variables

### 4. Deploy Your Application

1. Click on "Manual Deploy" and select "Deploy latest commit"
2. Render will build and deploy your application

### 5. Access Your Application

Once deployment is complete, you can access your application at the URL provided by Render.

## Understanding the Configuration

### Modified Files

1. **config.py**: Updated to use environment variables for Redis connection
2. **requirements.txt**: Added Redis and Gunicorn dependencies
3. **render.yaml**: Configuration file for Render deployment
4. **Procfile**: Specifies how to run the application

### Redis Connection

In production, your application will automatically connect to the Redis instance provided by Render using the environment variables configured in the `render.yaml` file.

## Troubleshooting

- **Application fails to start**: Check the logs in the Render dashboard for error messages
- **Redis connection issues**: Verify that the Redis service is running and properly connected
- **API key issues**: You may need to generate new API keys after deployment

## Local Development vs. Production

The updated configuration allows your application to work both locally and in production:

- **Local**: Uses localhost Redis connection
- **Production**: Uses Render-provided Redis instance via environment variables

No code changes are needed when switching between environments.