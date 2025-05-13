import fs from 'fs';
import { execSync } from 'child_process';

const certPath = './certs/selfsigned.crt';
const keyPath = './certs/selfsigned.key';

if (!fs.existsSync(certPath) || !fs.existsSync(keyPath)) {
  execSync(`
    mkdir -p certs && \
    openssl req -x509 -newkey rsa:4096 -sha256 -days 365 -nodes \
    -keyout ${keyPath} \
    -out ${certPath} \
    -subj "/CN=localhost"
  `);
  console.log('Сертификат создан');
} else {
  console.log('Сертификаты уже существуют');
}
