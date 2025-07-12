import cloudinary
import cloudinary.uploader

cloudinary.config(
  cloud_name='diqyqtjql',
  api_key='981637827458533',
  api_secret='EA6rcllbxaPF6G9SswqjoWnVrCk'
  # for production
  # cloud_name='dh2h6ia0n',
  # api_key='853734915947643',
  # api_secret='X9p-pAu7ZNjDnQEnx0_HMFuLl0o'
)

def upload_to_cloudinary(file, folder='user'):
    result = cloudinary.uploader.upload(file, folder=folder,resource_type="auto")
    return result['secure_url']
