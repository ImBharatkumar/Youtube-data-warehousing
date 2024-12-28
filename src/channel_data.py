# Import necessary libraries
from googleapiclient.discovery import build
import os, json
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variable
api_key = os.getenv('YOUTUBE_API_KEY')

# Check if the API key was successfully retrieved
if api_key:
    print("API Key:", api_key)
else:
    print("Error: YOUTUBE_API_KEY environment variable not set.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/sushidolly/.config/gcloud/application_default_credentials.json"

# Function to retrieve channel data
def get_channel_data(channel_id,api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    # Retrieve channel information
    channels_response = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()

    if 'items' not in channels_response or len(channels_response['items']) == 0:
        print("Channel not found.")
        return None

    channel = channels_response['items'][0]
    channel_name = channel['snippet']['title']
    subscriber_count = int(channel['statistics']['subscriberCount'])
    channel_views = int(channel['statistics']['viewCount'])
    channel_description = channel['snippet']['description']

    # Retrieve playlists
    playlists = []
    next_page_token = None
    while True:
        playlists_response = youtube.playlists().list(
            part='snippet',
            channelId=channel_id,
            maxResults=10,  # Increase or decrease as needed
            pageToken=next_page_token
        ).execute()

        if 'items' in playlists_response:
            playlists.extend(playlists_response['items'])

        next_page_token = playlists_response.get('nextPageToken')
        if not next_page_token:
            break

    if len(playlists) == 0:
        print("No playlists found.")
        return None

    videos = {}
    for playlist in playlists:
        playlist_id = playlist['id']
        playlist_name = playlist['snippet']['title']

        # Retrieve videos for the playlist
        videos_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=10  # Increase or decrease as needed
        ).execute()

        for video_item in videos_response['items']:
            video_id = video_item['snippet']['resourceId']['videoId']

            # Retrieve video details
            video_details_response = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            ).execute()

            if 'items' not in video_details_response or len(video_details_response['items']) == 0:
                print(f"Video not found: {video_id}")
                continue

            video = video_details_response['items'][0]
            video_name = video['snippet']['title']
            video_description = video['snippet']['description']
            tags = video['snippet']['tags'] if 'tags' in video['snippet'] else []
            published_at = video['snippet']['publishedAt']
            view_count = int(video['statistics']['viewCount'])
            like_count = int(video['statistics']['likeCount'])
            dislike_count = int(video['statistics'].get('dislikeCount', 0))  # Handle missing 'dislikeCount' key
            favorite_count = int(video['statistics']['favoriteCount'])
            comment_count = int(video['statistics']['commentCount'])
            duration = video['contentDetails']['duration']
            thumbnail = video['snippet']['thumbnails']['default']['url']
            caption_status = video['snippet']['localized'].get('isCaptionAvailable',
                                                               False)  # Handle missing 'isCaptionAvailable' key

            video_data = {
                'video_id': video_id,
                'video_name': video_name,
                'video_description': video_description,
                'tags': tags,
                'published_at': published_at,
                'view_count': view_count,
                'like_count': like_count,
                'dislike_count': dislike_count,
                'favorite_count': favorite_count,
                'comment_count': comment_count,
                'duration': duration,
                'thumbnail': thumbnail,
                'caption_status': caption_status,
                'Playlist_name': playlist_name,
                'playlist_id': playlist_id
            }
            videos[video_id] = video_data

    # Return channel data and video information
    channel_data = {
        'channel_name': {
            'channel_name': channel_name,
            'channel_id': channel_id,
            'subscription_count': subscriber_count,
            'channel_views': channel_views,
            'channel_description': channel_description,
            'playlists': []
        },
        **videos
    }

    for playlist in playlists:
        playlist_id = playlist['id']
        playlist_name = playlist['snippet']['title']
        channel_data['channel_name']['playlists'].append({
            'playlist_id': playlist_id,
            'playlist_name': playlist_name
        })

    with open("data/channel_data.json", "w") as f:
        json.dump(channel_data, f, indent=4)
        print("Data saved to channel_data.json")



