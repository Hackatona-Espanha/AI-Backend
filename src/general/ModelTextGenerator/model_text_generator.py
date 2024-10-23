
import json
import logging
from botocore.exceptions import ClientError
import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Claude3SonnetInvoker:
    """
    Class responsible for invoking the Anthropic Claude 2.1 model through the AWS Bedrock Runtime service.
    
    It encapsulates the functionality to send a prompt to the specified model and process the generated response,
    making it simpler to interact with artificial intelligence models hosted in the cloud.

    Attributes:
        boto3_bedrock (boto3.Client): Client for interacting with the AWS Bedrock Runtime service.
    
    Methods:
        __init__(self): Builder that initializes the AWS Bedrock Runtime client.
        invoke_claude(self, prompt): Method to invoke the model with a specific prompt and get the response.
    """
    
    def __init__(self):
        """
        Launches the Claude 3 sonnet invoker, configuring the AWS Bedrock Runtime client.
        """
        self.boto3_bedrock = boto3.client(service_name="bedrock-runtime")
    
    def invoke_claude(self, prompt):
        """
        Invokes the Anthropic Claude 3 sonnet model to perform an inference
        using the prompt provided in the request body.

        :param prompt: The prompt you want Claude to complete.
        :return: The model inference answer.
        :Raises: ClientError: If an error occurs while invoking the model.
        """
        prompt_config = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        }

        body = json.dumps(prompt_config)

        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
        accept = "application/json"
        contentType = "application/json"

        response = self.boto3_bedrock.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())

        results = response_body.get("content")[0].get("text")
        return results