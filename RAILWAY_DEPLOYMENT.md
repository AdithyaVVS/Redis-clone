# Deploying Redis Clone API on Railway

This guide will walk you through deploying your Redis Clone API on Railway.app, which offers a free tier without requiring payment information upfront.

## Prerequisites

- A [Railway](https://railway.app) account (sign up with GitHub)
- Your project code pushed to a GitHub repository

## Deployment Steps

### 1. Push Your Code to GitHub

Make sure your code is pushed to a GitHub repository that Railway can access.

### 2. Set Up Your Project on Railway

1. Log in to your Railway account (sign up with GitHub if you don't have an account)
2. Click on "New Project" and select "Deploy from GitHub repo"
3. Connect your GitHub account and select your Redis Clone repository
4. Railway will automatically detect the `railway.json` configuration file

### 3. Add a Redis Plugin

1. In your project dashboard, click on "+ New"
2. Select "Database" and then "Redis"
3. Railway will provision a Redis instance for your project

### 4. Link Your Services

1. Go to your web service settings
2. Navigate to the "Variables" tab
3. Railway automatically provides environment variables for connected services
4. Ensure the following variables are set (they should be automatically populated):
   - `REDIS_URL` - The full connection URL for your Redis instance
   - `PORT` - The port your application will run on

### 5. Deploy Your Application

1. Railway will automatically deploy your application when you push changes to your repository
2. You can also manually deploy from the Railway dashboard

### 6. Access Your Application

Once deployment is complete, you can access your application at the URL provided by Railway in the "Deployments" tab.

## Understanding the Configuration

### Modified Files

1. **config.py**: Updated to use Railway's environment variables for Redis connection
2. **railway.json**: Configuration file for Railway deployment
3. **Procfile**: Already compatible with Railway (no changes needed)

### Redis Connection

In production, your application will automatically connect to the Redis instance provided by Railway using the environment variables.

## Troubleshooting

- **Application fails to start**: Check the logs in the Railway dashboard for error messages
- **Redis connection issues**: Verify that the Redis plugin is properly installed and connected
- **API key issues**: You may need to generate new API keys after deployment

## Local Development vs. Production

The updated configuration allows your application to work both locally and in production:

- **Local**: Uses localhost Redis connection
- **Production**: Uses Railway-provided Redis instance via environment variables

No code changes are needed when switching between environments.