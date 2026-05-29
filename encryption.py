from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os
import logging

# =========================
# Logging Setup
# =========================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# =========================
# Paths
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_DIR = os.path.join(BASE_DIR, "secret")

KEY_PATH = os.path.join(SECRET_DIR, "secret.key")

# =========================
# Generate Key
# =========================

def generate_key():

    try:
        os.makedirs(SECRET_DIR, exist_ok=True)

        if not os.path.exists(KEY_PATH):

            key = Fernet.generate_key()

            with open(KEY_PATH, "wb") as key_file:

                key_file.write(key)
            
            logger.info("Security key generated successfully")

    except Exception as e:
        logger.error(f"Error generating key: {str(e)}")
        raise

# =========================
# Load Key
# =========================

def load_key():

    try:
        if not os.path.exists(KEY_PATH):

            generate_key()

        with open(KEY_PATH, "rb") as key_file:

            return key_file.read()
    
    except Exception as e:
        logger.error(f"Error loading key: {str(e)}")
        raise

# =========================
# Encrypt Folder
# =========================

def encrypt_folder(folder_path):

    try:
        if not os.path.exists(folder_path):
            logger.error(f"Folder not found: {folder_path}")
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        key = load_key()

        cipher = Fernet(key)

        encrypted_count = 0

        for root_folder, folders, files in os.walk(folder_path):

            for filename in files:

                file_path = os.path.join(root_folder, filename)

                if file_path.endswith(".enc"):
                    continue

                try:

                    with open(file_path, "rb") as file:

                        data = file.read()

                    encrypted_data = cipher.encrypt(data)

                    encrypted_file = file_path + ".enc"

                    with open(encrypted_file, "wb") as file:

                        file.write(encrypted_data)

                    os.remove(file_path)

                    encrypted_count += 1
                    
                    logger.info(f"Encrypted: {filename}")

                except PermissionError:
                    logger.warning(f"Permission denied for file: {file_path}")
                except Exception as e:
                    logger.error(f"Error encrypting {file_path}: {str(e)}")

        logger.info(f"Encryption completed. Total files encrypted: {encrypted_count}")
        return encrypted_count
    
    except Exception as e:
        logger.error(f"Encryption process failed: {str(e)}")
        raise

# =========================
# Decrypt Folder
# =========================

def decrypt_folder(folder_path):

    try:
        if not os.path.exists(folder_path):
            logger.error(f"Folder not found: {folder_path}")
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        key = load_key()

        cipher = Fernet(key)

        decrypted_count = 0

        for root_folder, folders, files in os.walk(folder_path):

            for filename in files:

                file_path = os.path.join(root_folder, filename)

                if not file_path.endswith(".enc"):
                    continue

                try:

                    with open(file_path, "rb") as file:

                        encrypted_data = file.read()

                    decrypted_data = cipher.decrypt(encrypted_data)

                    original_file = file_path[:-4]

                    with open(original_file, "wb") as file:

                        file.write(decrypted_data)

                    os.remove(file_path)

                    decrypted_count += 1
                    
                    logger.info(f"Decrypted: {filename}")

                except InvalidToken:
                    logger.error(f"Invalid encryption token for: {file_path}")
                except PermissionError:
                    logger.warning(f"Permission denied for file: {file_path}")
                except Exception as e:
                    logger.error(f"Error decrypting {file_path}: {str(e)}")

        logger.info(f"Decryption completed. Total files decrypted: {decrypted_count}")
        return decrypted_count
    
    except Exception as e:
        logger.error(f"Decryption process failed: {str(e)}")
        raise