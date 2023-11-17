
import os

def generate_random_psk(psk_length):
    import secrets

    if psk_length % 2 != 0:
        raise ValueError("The length of the PSK must be an even number")
    
    psk = secrets.token_hex(psk_length // 2)
    return psk

def share_psk_to(psk, address):
    with open(f"./subnet_{address}/key.psk", "w") as f:
        f.write(psk)

if __name__ == "__main__":
    psk = generate_random_psk(32)
    share_psk_to(psk, "a")
    share_psk_to(psk, "b")