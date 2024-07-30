import json

def encode_message(message):
    """
    Encode a message for network transmission.
    """
    return json.dumps(message).encode('utf-8')

def decode_message(data):
    """
    Decode a received message.
    """
    return json.loads(data.decode('utf-8'))

# Define message types
MESSAGE_TYPES = {
    'CONNECT': 'connect',
    'DISCONNECT': 'disconnect',
    'RESOURCE_UPDATE': 'resource_update',
    'TRAINING_TASK': 'training_task',
    'TRAINING_RESULT': 'training_result',
}

def create_message(message_type, payload):
    """
    Create a structured message.
    """
    if message_type not in MESSAGE_TYPES.values():
        raise ValueError(f"Invalid message type: {message_type}")
    
    return {
        'type': message_type,
        'payload': payload
    }