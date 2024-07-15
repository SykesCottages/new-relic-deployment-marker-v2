Certainly! Here's a README template based on the AWS CodeDeploy pipe example, tailored for your "New Relic Deployment Marker" Bitbucket Pipe:

---

# New Relic Deployment Marker Bitbucket Pipe

## Description

This Bitbucket Pipe helps you add deployment markers to New Relic APM. It finds the application ID in New Relic based on the application name and component type, then adds a deployment marker.

## YAML Definition

Add the following snippet to the `script` section of your `bitbucket-pipelines.yml` file:

```yaml
- pipe: github.com/SykesCottages/bitbucket-pipes@1.0.0
  variables:
    NEW_RELIC_API_KEY: '<string>' # Required. New Relic API Key.
    SYSTEM_NAME: '<string>' # Required. The name of the application to find the ID for.
    COMPONENT_TYPE: '<string>' # Required. The component type of the application to find the ID for. Options are Web, Cmd, and Cron.
    ENVIRONMENT: '<string>' # Optional. Environment name.
    REGION: '<string>' # Optional. Region name.
    DEPLOYMENT_REVISION: '<string>' # Optional. Bitbucket commit hash for the deployment.
```

## Variables

| Variable            | Usage                                                                                                                                                                                                                   |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| NEW_RELIC_API_KEY   | New Relic API Key.                                                                                                                                                                                                      |
| SYSTEM_NAME         | The name of the application in New Relic to find the ID for.                                                                                                                                                             |
| COMPONENT_TYPE      | The component type of the application in New Relic. Valid options are Web, Cmd, and Cron.                                                                                                                                |
| ENVIRONMENT         | Environment name where the deployment is taking place (e.g., production, staging).                                                                                                                                       |
| REGION              | Region name where the application is deployed (e.g., us-west-1).                                                                                                                                                        |
| DEPLOYMENT_REVISION | Bitbucket commit hash used as the deployment revision identifier.                                                                                                                                                        |

## Examples

### Basic Usage

Add a deployment marker to New Relic for an application named "MyApp" of type "Web", deployed to production:

```yaml
script:
  - pipe: github.com/SykesCottages/bitbucket-pipes@1.0.0
    variables:
      NEW_RELIC_API_KEY: $NEW_RELIC_API_KEY
      SYSTEM_NAME: 'MyApp'
      COMPONENT_TYPE: 'Web'
      ENVIRONMENT: 'production'
      REGION: 'us-west-1'
      DEPLOYMENT_REVISION: $BITBUCKET_COMMIT
```

### Minimal Configuration

A minimal configuration to add a deployment marker, assuming environment variables are set for API key, region, and deployment revision:

```yaml
script:
  - pipe: github.com/SykesCottages/bitbucket-pipes@1.0.0
    variables:
      SYSTEM_NAME: 'MyApp'
      COMPONENT_TYPE: 'Web'
```

### Notes

- Replace placeholders like `$NEW_RELIC_API_KEY`, `$SYSTEM_NAME`, and `$BITBUCKET_COMMIT` with actual values or variables defined in your Bitbucket Pipelines environment.
- Ensure that the New Relic API key has sufficient permissions to add deployment markers.
- Adjust the `REGION` and `ENVIRONMENT` variables based on your deployment setup.

## Repository

- **GitHub Repository:** [SykesCottages/bitbucket-pipes](https://github.com/SykesCottages/bitbucket-pipes)

## Vendor and Maintainer

- **Vendor:** NewRelic
- **Maintainer:** Sykes Cottages

## Tags

- deployment
- NewRelic

---

This README provides a structured guide for using your Bitbucket Pipe to add deployment markers to New Relic. Make sure to update version numbers, links, and additional details specific to your pipe as necessary.