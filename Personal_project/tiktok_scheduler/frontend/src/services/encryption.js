import CryptoJS from 'crypto-js';

// Generate a random key
const generateEncryptionKey = () => {
  return CryptoJS.lib.WordArray.random(256 / 8).toString();
};

// Derive a key from a password using PBKDF2
const deriveKeyFromPassword = (password, salt = null) => {
  if (!salt) {
    salt = CryptoJS.lib.WordArray.random(128 / 8).toString();
  }
  
  const key = CryptoJS.PBKDF2(password, salt, {
    keySize: 256 / 32,
    iterations: 1000
  }).toString();
  
  return { key, salt };
};

// Encrypt data with a key
const encryptData = (data, key) => {
  if (typeof data !== 'string') {
    data = JSON.stringify(data);
  }
  
  const encrypted = CryptoJS.AES.encrypt(data, key).toString();
  return encrypted;
};

// Decrypt data with a key
const decryptData = (encryptedData, key) => {
  try {
    const decrypted = CryptoJS.AES.decrypt(encryptedData, key).toString(CryptoJS.enc.Utf8);
    
    // Try to parse as JSON if possible
    try {
      return JSON.parse(decrypted);
    } catch (e) {
      return decrypted;
    }
  } catch (error) {
    console.error('Decryption failed:', error);
    return null;
  }
};

// Encrypt a token using the user's password
const encryptToken = (token, password) => {
  // First derive a key from the password
  const { key, salt } = deriveKeyFromPassword(password);
  
  // Encrypt the token
  const encrypted = encryptData(token, key);
  
  // Return the encrypted data along with the salt
  return {
    encrypted,
    salt
  };
};

// Decrypt a token using the user's password and salt
const decryptToken = (encryptedData, password, salt) => {
  // Derive the key from the password and salt
  const { key } = deriveKeyFromPassword(password, salt);
  
  // Decrypt the token
  return decryptData(encryptedData, key);
};

// Hash a password (for local verification only, not for storage)
const hashPassword = (password) => {
  return CryptoJS.SHA256(password).toString();
};

export default {
  generateEncryptionKey,
  deriveKeyFromPassword,
  encryptData,
  decryptData,
  encryptToken,
  decryptToken,
  hashPassword
};