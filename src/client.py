import boto3
from langchain_aws import ChatBedrock


def create_client():
    """Create and return a Bedrock runtime client."""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )


def create_llm(client):
    """Create and return a ChatBedrock LLM instance."""
    return ChatBedrock(
        model_id="us.amazon.nova-lite-v1:0",
        client=client,
        model_kwargs={"max_tokens": 1500, "temperature": 0.7}
    )
