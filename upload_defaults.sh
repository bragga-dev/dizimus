#!/bin/sh
# upload_defaults.sh
# Sobe as imagens padrão para o bucket dizimus-media no MinIO.
# Execute UMA VEZ após subir os containers:
#   chmod +x upload_defaults.sh && ./upload_defaults.sh

set -e

MINIO_URL="http://localhost:9000"
MINIO_USER="minioadmin"
MINIO_PASS="minioadmin123"
BUCKET="dizimus-media"

# Cria pasta local de defaults se não existir
mkdir -p default

# Se você não tiver as imagens, cria placeholders mínimos (PNG 1x1 cinza)
if [ ! -f "default/user_img.jpg" ]; then
  echo "⚠️  default/user_img.jpg não encontrado — criando placeholder..."
  python3 -c "
from PIL import Image
img = Image.new('RGB', (200, 200), color=(200, 200, 200))
img.save('default/user_img.jpg')
print('  ✓ default/user_img.jpg criado')
"
fi

if [ ! -f "default/banner.jpg" ]; then
  echo "⚠️  default/banner.jpg não encontrado — criando placeholder..."
  python3 -c "
from PIL import Image
img = Image.new('RGB', (1200, 400), color=(180, 180, 180))
img.save('default/banner.jpg')
print('  ✓ default/banner.jpg criado')
"
fi

echo "📦 Configurando MinIO client..."
docker run --rm --network host \
  minio/mc:latest \
  alias set local "$MINIO_URL" "$MINIO_USER" "$MINIO_PASS"

echo "⬆️  Enviando imagens padrão para o bucket $BUCKET..."
docker run --rm --network host \
  -v "$(pwd)/default:/default" \
  minio/mc:latest \
  cp /default/user_img.jpg "local/$BUCKET/default/user_img.jpg"

docker run --rm --network host \
  -v "$(pwd)/default:/default" \
  minio/mc:latest \
  cp /default/banner.jpg "local/$BUCKET/default/banner.jpg"

echo "✅ Imagens padrão enviadas com sucesso!"
echo "   → $MINIO_URL/$BUCKET/default/user_img.jpg"
echo "   → $MINIO_URL/$BUCKET/default/banner.jpg"