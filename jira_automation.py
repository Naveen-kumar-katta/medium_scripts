import requests
from requests.auth import HTTPBasicAuth
import json
import traceback

# Base URL for Jira instance
jira_url = 'https://_____.atlassian.net/'

# Jira user email and API token for authentication
jira_user = 'MAIL'
jira_token = 'JIRA_TOKEN'

# Endpoint URLs for creating issues and searching users
create_issue_url = f'{jira_url}/rest/api/2/issue'
get_user_url = f'{jira_url}/rest/api/3/user/search'

def get_assignee_account_id(developer_email):
    """
    Retrieve the Jira account ID of a user based on their email address.

    Args:
        developer_email (str): The email address of the developer.

    Returns:
        str: The Jira account ID of the user if found, otherwise None.
    """
    try:
        # Parameters for user search query
        params = {
            'query': developer_email
        }

        # Make a GET request to Jira's user search API
        response = requests.get(
            get_user_url,
            params=params,
            headers={'Accept': 'application/json'},
            auth=HTTPBasicAuth(jira_user, jira_token)
        )

        # Check if the request was successful
        if response.status_code == 200:
            users = response.json()
            # Iterate through the user list and return the account ID of the first matching user
            for user in users:
                return user['accountId']
        else:
            # Print error message if the request failed
            print('Failed to get user info:', response.status_code, response.text)
    except Exception as e:
        # Print stack trace for any exceptions that occur
        print('An error occurred while retrieving user information:')
        print(traceback.format_exc())

    return None

def create_jira(project, summary, description, issue_type, assignee_account_id):
    """
    Create a new Jira issue with the specified details.

    Args:
        project (str): The project key where the issue will be created.
        summary (str): A brief summary or title of the issue.
        description (str): A detailed description of the issue.
        issue_type (str): The type of issue (e.g., Bug, Task).
        assignee_account_id (str): The Jira account ID of the user to assign the issue to.

    Returns:
        bool: True if the issue was created successfully, otherwise False.
    """
    try:
        # Define headers for the HTTP request
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Construct the payload for the new Jira issue
        payload = {
            "fields": {
                "project": {
                    "key": project  # Project key where the issue will be created
                },
                "summary": summary,  # Brief summary of the issue
                "description": description,  # Detailed description of the issue
                "issuetype": {
                    "name": issue_type  # Type of the issue (e.g., Bug, Task)
                },
                "assignee": {
                    "id": assignee_account_id  # Account ID of the assignee
                }
            }
        }

        # Make a POST request to the Jira API to create the issue
        response = requests.post(
            create_issue_url,  # URL endpoint for creating issues
            data=json.dumps(payload),  # Convert payload to JSON format
            headers=headers,  # HTTP headers
            auth=HTTPBasicAuth(jira_user, jira_token)  # Authentication
        )

        # Check if the issue was created successfully (HTTP status code 201)
        if response.status_code == 201:
            return True  # Issue created successfully
        else:
            # Print error message and return False if creation failed
            print('Failed to create Jira issue. Status:', response.status_code, 'Response:', response.text)
            return False
    except Exception as e:
        # Print stack trace for any exceptions that occur
        print('An error occurred while creating the Jira issue:')
        print(traceback.format_exc())
        return False

if __name__ == '__main__':
    # Define variables for the issue details
    developer_email = 'ASSIGNEE_EMAIL_ADDRESS'
    project = 'PROJECT_KEY'
    summary = 'Issue Summary'
    description = 'Detailed description of the issue'
    issue_type = 'Issue Type'  # E.g., Bug, Task

    # Fetch the Jira account ID for the specified developer email
    assignee_account_id = get_assignee_account_id(developer_email)
    
    # Check if the assignee was found
    if assignee_account_id is None:
        print('Developer Email not found.')
    else:
        # Create a Jira issue and check if it was successful
        issue_created = create_jira(project, summary, description, issue_type, assignee_account_id)
        if issue_created:
            print('Ticket created successfully.')
        else:
            print('Failed to create ticket.')
