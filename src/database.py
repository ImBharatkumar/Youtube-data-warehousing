# import libraries
from sqlalchemy import create_engine
from table_schema import create_tables
from table_schema import insert_channel_data, insert_playlist_data, insert_video_data
from utility import convert_iso_to_mysql_datetime, convert_duration_to_seconds, connect_mysql, fetch_channel_data_from_mongodb



# write data into mysql
def write_to_sql():
    # Connect to MySQL
    engine = connect_mysql()
    
    # Create tables
    create_tables(engine)

    # Fetch channel data from MongoDB (implement this according to your needs)
    channel_data = fetch_channel_data_from_mongodb()
    
    # Insert channel data
    try:
        insert_channel_data(engine, {
            'id': channel_data['channel_name']['channel_id'],
            'name': channel_data['channel_name']['channel_name'],
            'subscription_count': channel_data['channel_name']['subscription_count'],
            'channel_views': channel_data['channel_name']['channel_views'],
            'channel_description': channel_data['channel_name']['channel_description']
        })
    except Exception as e:
        print(f"Error processing channel: {e}")




    # Prepare playlist data
    playlists_to_insert = []

    for playlist in channel_data['channel_name']['playlists']:
        try:
            playlists_to_insert.append({
                'playlist_id': playlist['playlist_id'],
                'channel_id': channel_data['channel_name']['channel_id'],
                'playlist_name': playlist['playlist_name']
            })
            # Now call insert_playlist_data with the complete list
            insert_playlist_data(engine, playlists_to_insert)

        except Exception as e:
            print(f"Error processing playlist: {e}")

    

    # Fetch channel data from MongoDB
    video_data = []

    # Iterate through keys in the document to find video entries
    for key, value in channel_data.items():
        if key != 'channel_name':  # Skip channel_name entry
            video_data.append(value)

    video_to_insert = []
    for video in video_data:
        try:
            # Prepare the video data for insertion
            video_to_insert.append({
                'video_id': video['video_id'],
                'playlist_id': video['playlist_id'],
                'video_name': video['video_name'],
                'published_at': convert_iso_to_mysql_datetime(video['published_at']),  # Correct key name
                'view_count': video['view_count'],
                'like_count': video['like_count'],  # Correct key name
                'dislike_count': video['dislike_count'],  # Correct key name
                'favorite_count': video['favorite_count'],
                'comment_count': video['comment_count'],
                'duration': convert_duration_to_seconds(video['duration']),  # Ensure this is an integer
                'thumbnail': video['thumbnail'],
                'caption_status': int(video['caption_status'])  # Convert boolean to int if necessary
            })
        except Exception as e:
            print(f"Error processing video: {e}")

    # Insert all videos at once after building the list
    for video_info in video_to_insert:
        try:
            insert_video_data(engine, video_info)
        except Exception as e:
            print(f"Error inserting video {video_info['video_id']}: {e}")
