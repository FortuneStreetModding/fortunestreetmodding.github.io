
function repeatKey(key: Uint8Array, contentLength: number): Uint8Array {
  const repeatedKey = new Uint8Array(contentLength);
  for (let i = 0; i < contentLength; i++) {
    repeatedKey[i] = key[i % key.length];
  }
  return repeatedKey;
}

export function concatenateKey(originalKey: Uint8Array, additionalKey: Uint8Array): Uint8Array {
  const extendedKey = new Uint8Array(originalKey.length + additionalKey.length);
  extendedKey.set(originalKey, 0);
  extendedKey.set(additionalKey, originalKey.length);
  return extendedKey;
}

export function encryptWithKey(content: ArrayBuffer, key: Uint8Array): Uint8Array {
  const extendedKey = repeatKey(key, content.byteLength);
  const contentBytes = new Uint8Array(content);
  const encryptedBytes = new Uint8Array(contentBytes.length);

  for (let i = 0; i < contentBytes.length; i++) {
    encryptedBytes[i] = contentBytes[i] ^ extendedKey[i];
  }

  return encryptedBytes;
}

export function decryptWithKey(encryptedContent: ArrayBuffer, key: Uint8Array): ArrayBuffer {
  const extendedKey = repeatKey(key, encryptedContent.byteLength);
  const encryptedBytes = new Uint8Array(encryptedContent);
  const decryptedBytes = new Uint8Array(encryptedBytes.length);

  for (let i = 0; i < encryptedBytes.length; i++) {
    decryptedBytes[i] = encryptedBytes[i] ^ extendedKey[i];
  }

  return decryptedBytes.buffer;
}

export function readFileAsArrayBuffer(file: File): Promise<ArrayBuffer> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as ArrayBuffer);
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

export async function computeSHA256(arrayBuffer: ArrayBuffer): Promise<ArrayBuffer> {
  const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
  return hashBuffer;
}

export function arrayBufferToHex(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  const hexArray = Array.from(bytes).map(byte => byte.toString(16).padStart(2, '0'));
  return hexArray.join('');
}

export async function download(url: string): Promise<ArrayBuffer> {
    // Fetch the file from the server
    const response = await fetch(url);

    // Check if the request was successful
    if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
    }

    return await response.arrayBuffer();
}