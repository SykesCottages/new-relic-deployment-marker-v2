import os
import requests
from typing import Dict, List, Any, Union


class Config:
    def __init__(self) -> None:
        self.new_relic_api_key: str = self.get_env_variable(
            'NEW_RELIC_API_KEY')
        self.system_name: str = self.get_env_variable('SYSTEM_NAME')
        self.component_type: str = self.get_env_variable('COMPONENT_TYPE')
        self.environment: str = self.get_env_variable('ENVIRONMENT')
        self.region: str = self.get_env_variable('REGION')
        self.deployment_user: str = os.getenv(
            'DEPLOYMENT_USER', 'bitbucket.pipeline')
        self.deployment_revision: str = self.get_env_variable(
            'DEPLOYMENT_REVISION')

    def get_env_variable(self, name: str) -> str:
        value = os.getenv(name)
        if value is None:
            raise ValueError(f"Environment variable {name} is not set.")
        return value

    def get_app_name_pattern(self) -> str:
        return f'%{self.system_name}%{self.environment}%{self.region}%{self.component_type}'


class NewRelicClient:
    def __init__(self, config: Config) -> None:
        self.api_key: str = config.new_relic_api_key
        self.base_url: str = 'https://api.newrelic.com/v2/'

    def search_applications(self, app_name_pattern: str) -> List[Dict[str, Any]]:
        headers: Dict[str, str] = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        url: str = f'{self.base_url}applications.json'
        params: Dict[str, str] = {
            'filter[name]': app_name_pattern
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['applications']

    def create_deployment_marker(self, app_id: str, user: str, revision: str, description: str) -> None:
        url: str = f'{self.base_url}applications/{app_id}/deployments.json'
        headers: Dict[str, str] = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        payload: Dict[str, Union[str, Dict[str, str]]] = {
            'deployment': {
                'revision': revision,
                'changelog': description,
                'user': user
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()


def main() -> None:
    try:
        config: Config = Config()
    except ValueError as e:
        print(f"Error initializing Config: {str(e)}")
        return

    client: NewRelicClient = NewRelicClient(config)

    # Example search pattern
    app_name_pattern: str = config.get_app_name_pattern()
    print(f"Searching applications with pattern: {app_name_pattern}")

    try:
        applications: List[Dict[str, Any]
                           ] = client.search_applications(app_name_pattern)

        for app in applications:
            app_id: str = app['id']
            app_name: str = app['name']
            print(f"Application ID: {app_id}, Name: {app_name}")

            # Example deployment marker
            deployment_description: str = "Deployed new version"
            client.create_deployment_marker(
                app_id, config.deployment_user, config.deployment_revision, deployment_description)
            print(f"Deployment marker created for Application ID {app_id}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
