import wave
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(filename)s] - %(message)s",
    handlers=[
        logging.FileHandler("./log/stegano.log"),
        logging.StreamHandler()
    ]
)

def encode(source_file: str, destination_file: str, message: str):
    try:
        print(source_file, message)
        song = wave.open(source_file, mode='rb')
        print(song)

        nframes=song.getnframes()
        frames=song.readframes(nframes)
        frame_list=list(frames)
        frame_bytes=bytearray(frame_list)

        res = ''.join(format(i, '08b') for i in bytearray(message, encoding ='utf-8'))
        print(res)
        logging.info("Length of binary after conversion: %s", str(len(res)))
        logging.info("Length of source file: %s", str(len(frame_bytes)))

        message = message + '*^*^*'
    except Exception as e:
        logging.error("Could not read source file or message: %s", str(e))

    try:
        result = []
        for c in message:
            bits = bin(ord(c))[2:].zfill(8)
            result.extend([int(b) for b in bits])

        j = 0
        for i in range(0,len(result),1): 
            #TODO: Change logic here later!!
            res = bin(frame_bytes[j])[2:].zfill(8)
            if res[len(res)-4]== result[i]:
                frame_bytes[j] = (frame_bytes[j] & 253)      #253: 11111101
            else:
                frame_bytes[j] = (frame_bytes[j] & 253) | 2
                frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
            j = j + 1
        
        frame_modified = bytes(frame_bytes)
    except Exception as e:
        logging.error("Could not embed message in the file properly: %s", str(e))

    try:
        with wave.open(destination_file, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)
        logging.info("Succesfuly encoded message to file %s", destination_file)
    except Exception as e:
        logging.error("Could not write to file: %s", str(e))

    song.close()

def decode(source_file):
    try:
        song = wave.open(source_file, mode='rb')

        nframes=song.getnframes()
        frames=song.readframes(nframes)
        frame_list=list(frames)
        frame_bytes=bytearray(frame_list)
    except Exception as e:
        logging.error("Could not read source file for decoding: %s", str(e))

    extracted = ""
    try:
        for i in range(len(frame_bytes)):
            res = bin(frame_bytes[i])[2:].zfill(8)
            if res[len(res)-2]==0:
                extracted+=res[len(res)-4]
            else:
                extracted+=res[len(res)-1]
        
            all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
            decoded_data = ""
            for byte in all_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    return decoded_data[:-5]

    except Exception as e:
        logging.error("Could not decode message in source file: %s", str(e))
