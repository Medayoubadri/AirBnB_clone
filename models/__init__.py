from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()  # Load any existing data from file.json, if it exists
