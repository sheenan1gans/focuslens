import sqlalchemy as db
import kagglehub

# Download latest version
path = kagglehub.dataset_download("groleo/european-football-database")


engine = db.create_engine(path)

conn = engine.connect()

#Acccessing the table

metadata = db.MetaData() #extracting metadata
divsion = db.Table('divisions', metadata, autoload_with = engine) #Table object

#print divisions metadata
print(repr(metadata.tables['divisions']))
