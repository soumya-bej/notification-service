from .redis_client import redis_client


def render_template(message, variables):
    for key, value in variables.items():
        message = message.replace(f"{{{{{key}}}}}", str(value))
    return message


def check_rate_limit(user_id):
    key = f"rate_limit:{user_id}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 3600)

    if count > 100:
        return False

    return True