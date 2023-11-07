import os
from local_agent import get_psk_from_env


def generate_random_psk():
    import secrets

    psk_length = 32  # Change this to your desired length

    if psk_length % 2 != 0:
        raise ValueError("The length of the PSK must be an even number")
    
    psk = secrets.token_hex(psk_length // 2)
    return psk

def export_psk_to_env():
    os.environ["PSK_GLOBAL"] = generate_random_psk()

def share_psk():
    psk = generate_random_psk()
    with open("./assets/key.psk", 'w') as f:
        f.write(psk)

if __name__ == '__main__':
    # export_psk_to_env()
    share_psk()
