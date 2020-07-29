from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings

def main():
  upload_file_path = 'a3a38d7a-6894-4448-847c-9010a8d73397.mp4'
  blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=foosballmediaservices;AccountKey=7EpDxeJTFbHS0uj5ecrpryHF7bGkrJKkG5Um6k0A8emH2uN0SNMUHQzdezg3+c+V6lDjNoIiA4CdJaE8cA9tIA==;EndpointSuffix=core.windows.net')
  blob = blob_service_client.get_blob_client(container='recordings', blob=upload_file_path)

  with open(upload_file_path, "rb") as data:
    blob.upload_blob(data, content_settings = ContentSettings(content_type='video/mp4'))
  
  print(blob.url)

if __name__ == '__main__':
	main()