from ocrspace_client import Configuration, RunClient

client_configuration = Configuration()
client_configuration.SetImageFilePath("c:\\Users\\astro\\OneDrive\\Desktop\\OCRspace-Client-App\\test\\scripture-1.png")
client_configuration.SetOCREngineNumber(3)
client_configuration.SetLanguage("eng")
client_configuration.SetScale(True)
RunClient(client_configuration)
