import cloudinary
import cloudinary.uploader

class UploadFileService:
    DEFAULT_AVATAR_HEIGHT: int = 250
    DEFAULT_AVATAR_WIDTH: int = 250
    
    def __init__(self, cloud_name, api_key, api_secret):
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True,
        )

    @staticmethod
    def upload_file(file, username) -> str:
        public_id = f"RestApp/{username}"
        r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=UploadFileService.DEFAULT_AVATAR_WIDTH, height=UploadFileService.DEFAULT_AVATAR_HEIGHT, crop="fill", version=r.get("version")
        )
        return src_url