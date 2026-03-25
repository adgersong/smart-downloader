"""
凭证加密模块 - AES-256 加密/解密
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class CredentialEncryptor:
    """凭证加密器 - AES-256"""
    
    def __init__(self, secret_key: str = None):
        """
        初始化加密器
        
        Args:
            secret_key: 密钥字符串，如不提供则从环境变量读取
        """
        self.secret_key = secret_key or os.getenv("ENCRYPTION_KEY")
        
        if not self.secret_key:
            # 生成新密钥并保存
            self.secret_key = self._generate_key()
            os.environ["ENCRYPTION_KEY"] = self.secret_key
        
        self.fernet = Fernet(self.secret_key.encode())
    
    def _generate_key(self) -> str:
        """生成加密密钥"""
        return base64.urlsafe_b64encode(os.urandom(32)).decode()
    
    def encrypt(self, plaintext: str) -> str:
        """
        加密明文
        
        Args:
            plaintext: 待加密的明文
            
        Returns:
            加密后的密文 (base64 编码)
        """
        if not plaintext:
            return ""
        
        encrypted = self.fernet.encrypt(plaintext.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """
        解密密文
        
        Args:
            ciphertext: 待解密的密文 (base64 编码)
            
        Returns:
            解密后的明文
        """
        if not ciphertext:
            return ""
        
        try:
            decoded = base64.b64decode(ciphertext.encode())
            decrypted = self.fernet.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"解密失败：{str(e)}")
    
    def encrypt_dict(self, data: dict) -> dict:
        """
        加密字典中的所有字符串值
        
        Args:
            data: 待加密的字典
            
        Returns:
            加密后的字典
        """
        encrypted = {}
        for key, value in data.items():
            if isinstance(value, str):
                encrypted[key] = self.encrypt(value)
            elif isinstance(value, dict):
                encrypted[key] = self.encrypt_dict(value)
            else:
                encrypted[key] = value
        return encrypted
    
    def decrypt_dict(self, data: dict) -> dict:
        """
        解密字典中的所有字符串值
        
        Args:
            data: 待解密的字典
            
        Returns:
            解密后的字典
        """
        decrypted = {}
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    decrypted[key] = self.decrypt(value)
                except ValueError:
                    # 不是加密数据，保持原样
                    decrypted[key] = value
            elif isinstance(value, dict):
                decrypted[key] = self.decrypt_dict(value)
            else:
                decrypted[key] = value
        return decrypted


# 全局加密器实例
_encryptor = None


def get_encryptor() -> CredentialEncryptor:
    """获取全局加密器实例"""
    global _encryptor
    if _encryptor is None:
        _encryptor = CredentialEncryptor()
    return _encryptor


def encrypt_credential(value: str) -> str:
    """加密凭证"""
    return get_encryptor().encrypt(value)


def decrypt_credential(value: str) -> str:
    """解密凭证"""
    return get_encryptor().decrypt(value)
