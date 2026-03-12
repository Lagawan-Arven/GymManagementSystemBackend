import logging

logger = logging.getLogger(__name__)

def log_action(owner_id, action, resource, resource_id):

    logger.info(f'{owner_id} {action} {resource} - {resource_id}')

def log_message(message: str):
    logger.info(f'{message}')
