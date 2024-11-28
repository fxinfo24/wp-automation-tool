#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 21:32:22 2024

@author: thesaint
"""

# src/wordpress_poster.py
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client
from pathlib import Path
from typing import Dict, Optional
import logging
from datetime import datetime
import mimetypes

class WordPressPoster:
    def __init__(self, config_manager):
        self.config = config_manager.get_credentials('wordpress')
        self.client = Client(
            self.config['url'],
            self.config['username'],
            self.config['password']
        )
        self.media_dir = Path('data/media')
        self.media_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            filename=f'logs/wordpress_poster_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def create_post(self, content: Dict) -> str:
        try:
            post = WordPressPost()
            post.title = content['title']
            post.content = await self._prepare_content(content)
            post.post_status = content.get('status', 'publish')
            post.terms_names = await self._prepare_taxonomies(content)
            post.thumbnail = await self._upload_featured_image(content.get('featured_image'))
            
            # Create the post
            post_id = self.client.call(posts.NewPost(post))
            logging.info(f"Successfully created post with ID: {post_id}")
            return post_id
            
        except Exception as e:
            logging.error(f"Failed to create post: {str(e)}")
            raise
            
    async def _prepare_content(self, content: Dict) -> str:
        try:
            processed_content = content['content']
            
            # Handle additional images
            if content.get('content_images'):
                for img in content['content_images']:
                    image_id = await self._upload_media(img['data'], f"content-{img['id']}.jpg")
                    image_url = await self._get_media_url(image_id)
                    processed_content = self._insert_image(processed_content, image_url, img['description'])
                    
            # Handle YouTube video
            if content.get('video'):
                processed_content = self._insert_video(processed_content, content['video']['embed_code'])
                
            return processed_content
            
        except Exception as e:
            logging.error(f"Content preparation failed: {str(e)}")
            raise
            
    async def _upload_featured_image(self, image_data: Dict) -> Optional[str]:
        try:
            if not image_data:
                return None
                
            image_id = await self._upload_media(
                image_data['data'],
                f"featured-{image_data['id']}.jpg"
            )
            return image_id
            
        except Exception as e:
            logging.error(f"Featured image upload failed: {str(e)}")
            return None
            
    async def _upload_media(self, data: bytes, filename: str) -> str:
        try:
            # Prepare media data
            mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            media_data = {
                'name': filename,
                'type': mime_type,
                'bits': xmlrpc_client.Binary(data),
                'overwrite': True
            }
            
            # Upload to WordPress
            response = self.client.call(media.UploadFile(media_data))
            return response['id']
            
        except Exception as e:
            logging.error(f"Media upload failed: {str(e)}")
           