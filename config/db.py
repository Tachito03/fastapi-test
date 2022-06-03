from sqlalchemy import create_engine, MetaData

#engine = create_engine("mysql+pymysql://root:@localhost:3306/dbmails")
engine = create_engine("mysql+pymysql://admin_aws:db_mails05!_@dbmails.cqguuowfmb5g.us-west-1.rds.amazonaws.com:3306/db_mails")

meta = MetaData()

conn = engine.connect()