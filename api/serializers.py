from rest_framework import serializers

class StreamThumbnailSerializer(serializers.Serializer):
    small = serializers.URLField()
    medium = serializers.URLField()
    large = serializers.URLField()

class LiveStreamSerializer(serializers.Serializer):
    """Serializer for live stream data"""
    id = serializers.CharField()
    user_id = serializers.CharField()
    user_login = serializers.CharField()
    user_name = serializers.CharField()
    game_id = serializers.CharField(allow_null=True)
    game_name = serializers.CharField()
    title = serializers.CharField()
    viewer_count = serializers.IntegerField()
    started_at = serializers.DateTimeField()
    language = serializers.CharField()
    thumbnail_url = serializers.URLField()
    tags = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    is_mature = serializers.BooleanField()
    type = serializers.CharField()
    thumbnail = StreamThumbnailSerializer()
    hls_url = serializers.URLField(required=False, allow_null=True)   
    stream_url = serializers.URLField()
    profile_image_url = serializers.URLField(allow_null=True)

class StreamResponseSerializer(serializers.Serializer):
    """Serializer for stream response with pagination"""
    data = LiveStreamSerializer(many=True)
    pagination = serializers.DictField(child=serializers.CharField(allow_null=True))

class CategorySerializer(serializers.Serializer):
    """Serializer for game/category data"""
    id = serializers.CharField()
    name = serializers.CharField()
    box_art_url = serializers.URLField()
    igdb_id = serializers.CharField(allow_blank=True)
    thumbnail = StreamThumbnailSerializer()

class CategoryResponseSerializer(serializers.Serializer):
    """Serializer for category response with pagination"""
    data = CategorySerializer(many=True)
    pagination = serializers.DictField(child=serializers.CharField(allow_null=True))

class SidebarStreamSerializer(serializers.Serializer):
    """Serializer for minimal stream data for sidebar"""
    user_name = serializers.CharField()
    viewer_count = serializers.IntegerField()
    thumbnail_url = serializers.URLField()
    thumbnail = StreamThumbnailSerializer()
    stream_url = serializers.URLField()
    hls_url = serializers.URLField(required=False, allow_null=True) 

class SidebarResponseSerializer(serializers.Serializer):
    """Serializer for sidebar stream response with pagination"""
    data = SidebarStreamSerializer(many=True)
    pagination = serializers.DictField(child=serializers.CharField(allow_null=True))

class ChannelSerializer(serializers.Serializer):
    """Serializer for channel data from search"""
    id = serializers.CharField()
    broadcaster_login = serializers.CharField()
    display_name = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.URLField()
    is_live = serializers.BooleanField()

class VODSerializer(serializers.Serializer):
    """Serializer for VOD/video data"""
    id = serializers.CharField()
    user_id = serializers.CharField()
    user_login = serializers.CharField()
    user_name = serializers.CharField()
    title = serializers.CharField()
    created_at = serializers.DateTimeField()
    duration = serializers.CharField()
    view_count = serializers.IntegerField()
    url = serializers.URLField()
    thumbnail_url = serializers.URLField()
    hls_url = serializers.URLField(required=False, allow_null=True)  
    type = serializers.CharField()
    thumbnail = StreamThumbnailSerializer()

class SearchChannelResponseSerializer(serializers.Serializer):
    """Serializer for channel search response"""
    data = ChannelSerializer(many=True)
    pagination = serializers.DictField(child=serializers.CharField(allow_null=True))

class SearchGameResponseSerializer(serializers.Serializer):
    """Serializer for game search response"""
    data = CategorySerializer(many=True)
    pagination = serializers.DictField(child=serializers.CharField(allow_null=True))

class ChannelVODResponseSerializer(serializers.Serializer):
    """Serializer for channel VOD response"""
    data = VODSerializer(many=True)
    pagination = serializers.DictField(child=serializers.CharField(allow_null=True))

class ChannelLiveResponseSerializer(serializers.Serializer):
    """Serializer for channel live stream response"""
    data = LiveStreamSerializer(many=True)
    pagination = serializers.DictField(child=serializers.CharField(allow_null=True))