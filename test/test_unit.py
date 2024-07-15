import unittest
import os
from unittest import mock
from unittest.mock import patch, MagicMock
from pipe import pipe 

class TestConfig(unittest.TestCase):
    
    @patch('os.getenv')
    def test_get_env_variable_exists(self, mock_getenv):
        mock_getenv.return_value = 'dummy_value'
        config = pipe.Config()
        result = config.get_env_variable('TEST_VAR')
        self.assertEqual(result, 'dummy_value')

    @patch('os.getenv')
    def test_get_env_variable_not_exists(self, mock_getenv):
        mock_getenv.side_effect = lambda var_name: None
        with self.assertRaises(ValueError):
            config = pipe.Config()

    def mockenv(**envvars):
        return mock.patch.dict(os.environ, envvars)

    @mockenv(NEW_RELIC_API_KEY="dummy_api_key", 
             SYSTEM_NAME="System",
             COMPONENT_TYPE="Web",
             ENVIRONMENT="Production",
             REGION="US",
             DEPLOYMENT_REVISION="1234")
    def test_get_app_name_pattern(self):
        config = pipe.Config()
        result = config.get_app_name_pattern()
        self.assertEqual(result, '%System%Production%US%Web')

class TestNewRelicClient(unittest.TestCase):

    def setUp(self):
        self.config = MagicMock()
        self.config.new_relic_api_key = 'dummy_api_key'
        self.client = pipe.NewRelicClient(self.config)

    @patch('requests.get')
    def test_search_applications(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'applications': [{'id': '1234', 'name': 'TestApp'}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        app_name_pattern = '%TestApp%'
        result = self.client.search_applications(app_name_pattern)

        mock_get.assert_called_once_with(
            'https://api.newrelic.com/v2/applications.json',
            headers={
                'X-Api-Key': 'dummy_api_key',
                'Content-Type': 'application/json'
            },
            params={'filter[name]': app_name_pattern}
        )

        self.assertEqual(result, [{'id': '1234', 'name': 'TestApp'}])

    @patch('requests.post')
    def test_create_deployment_marker(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        app_id = '1234'
        user = 'test_user'
        revision = 'r1'
        description = 'Deployment description'

        self.client.create_deployment_marker(app_id, user, revision, description)

        mock_post.assert_called_once_with(
            f'https://api.newrelic.com/v2/applications/{app_id}/deployments.json',
            headers={
                'X-Api-Key': 'dummy_api_key',
                'Content-Type': 'application/json'
            },
            json={
                'deployment': {
                    'revision': revision,
                    'changelog': description,
                    'user': user
                }
            }
        )

if __name__ == '__main__':
    unittest.main()