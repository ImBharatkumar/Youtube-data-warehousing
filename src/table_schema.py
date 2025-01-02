from sqlalchemy import MetaData, engine, create_engine
from sqlalchemy import Table,text, Column, Integer, String, VARCHAR,TEXT, DATETIME, BigInteger
metadata_obj = MetaData()


# Define the table schema
channel_table = Table(
    "channel_data",
    metadata_obj, 
    Column("id", VARCHAR(255), primary_key=True),
    Column("name", VARCHAR(255)),
    Column("subscription_count", Integer),
    Column("channel_views",BigInteger),
    Column("channel_description", TEXT))

playlist_table = Table(
    "Playlist_data",
    metadata_obj,
    Column("playlist_id", VARCHAR(255), primary_key=True),
    Column("channel_id", VARCHAR(255)),
    Column("playlist_name",VARCHAR(255))
)

video_table = Table(
    "video_data",
    metadata_obj,
    Column("video_id", VARCHAR(255), primary_key=True),
    Column("playlist_id", VARCHAR(255)),
    Column("video_name", VARCHAR(255)),
    Column("Published_at", DATETIME),
    Column("view_count", Integer),
    Column("Like_count", Integer),
    Column("DisLike_count", Integer),
    Column("favorite_count", Integer),
    Column("comment_count", Integer),
    Column("duration", Integer),
    Column("thumbnail", VARCHAR(512)),
    Column("caption_status", VARCHAR(10))

)

# functions to create table
def create_tables(engine):
    metadata_obj.create_all(engine)
    print("Tables created successfully.")



# code to insert data
def insert_channel_data(engine, channel_info):
    with engine.connect() as conn:
        sql = text("""
            INSERT IGNORE INTO channel_data (id, name, subscription_count, channel_views, channel_description)
            VALUES (:id, :name, :subscription_count, :channel_views, :channel_description)
        """)
        conn.execute(sql, channel_info)
        conn.commit()
        print("Channel data inserted.")

def insert_playlist_data(engine, playlists):
    print(playlists)
    with engine.connect() as conn:
        sql = text("""
            INSERT IGNORE INTO Playlist_data (playlist_id, channel_id, playlist_name)
            VALUES (:playlist_id, :channel_id, :playlist_name)
        """)
        for playlist in playlists:
            conn.execute(sql, playlist)
        conn.commit()
        print("Playlist data inserted.")


def insert_video_data(engine, video_info):
    with engine.connect() as conn:
        sql = text("""
            INSERT IGNORE INTO video_data (video_id, playlist_id, video_name,
                                    published_at, view_count, like_count,
                                    dislike_count, favorite_count,
                                    comment_count, duration, thumbnail,
                                    caption_status)
            VALUES (:video_id, :playlist_id, :video_name,
                    :published_at, :view_count, :like_count,
                    :dislike_count, :favorite_count,
                    :comment_count, :duration, :thumbnail,
                    :caption_status)
        """)
        conn.execute(sql, video_info)
        conn.commit()
        print("Video data inserted.")
