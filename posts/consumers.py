import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Post, Comment
from profiles.models import Profile

class PostDetailConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_id = None
        self.post_group_id = None
        self.post = None
        self.profile = None

    def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_id = f'post_{self.post_id}'
        self.post = Post.objects.get(pk = self.post_id)
        self.profile = Profile.objects.get(user_id = self.scope['user'].pk)
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.post_group_id,
            self.channel_name
        )
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.post_group_id,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if not self.profile.user.is_authenticated:
            return
        
        text_data_json = json.loads(text_data)

        match text_data_json['type']:
            case 'comment':
                print(1)
                comment = Comment.objects.create(author=self.profile,text = text_data_json['text'])
                self.post.comments.add(comment)
                async_to_sync(self.channel_layer.group_send)(
                    self.post_group_id,
                    {
                        'type':'comment',
                        'profile':self.profile.user.username,
                        'profile_pic': self.profile.profile_pic.path,
                        'text': comment.text,
                        'comment_id':comment.pk
                    }
                )
            case 'post_like':
                if self.post.likes.contains(self.profile):
                    self.post.likes.remove(self.profile)
                else:
                    self.post.likes.add(self.profile)
            case 'comment_like':
                comment = Comment.objects.get(pk = int(text_data_json['comment_id']))
                if comment.likes.contains(self.profile):
                    comment.likes.remove(self.profile)
                else:
                    comment.likes.add(self.profile)
                pass
            case 'reply_to':
                profile = Profile.objects.get(pk = text_data_json['profile_id'])
                async_to_sync(self.channel_layer.group_send)(
                    self.post_group_id,
                    {
                        'type':'reply_to',
                        'profile_tag':profile.tag,
                        'profile_id':profile.pk,
                    }
                )
            case 'share':
                pass

    def comment(self, event):
        self.send(text_data=json.dumps(event))

class HomePageConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = None
        self.profile_group_id = None

    def connect(self):
        self.profile = Profile.objects.get(user_id = self.scope['user'].pk)
        self.profile_group_id = f'profile_{self.profile.pk}'
        self.accept()
        
        async_to_sync(self.channel_layer.group_add)(
            self.profile_group_id,
            self.channel_name
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.profile_group_id,
            self.channel_name
        )
        
    def receive(self, text_data=None, bytes_data=None):
        if not self.profile.user.is_authenticated:
            return
        
        text_data_json = json.loads(text_data)

        match text_data_json['type']:
            case 'homepage_like':
                post = Post.objects.get(pk = int(text_data_json['post_id']))
                if post.likes.contains(self.profile):
                    post.likes.remove(self.profile)
                else:
                    post.likes.add(self.profile)


    def post_like(self, event):
        self.send(text_data=json.dumps(event))