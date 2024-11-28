#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:07:25 2024

@author: thesaint
"""

# src/wordpress_integration.py
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
import logging
from typing import Dict, List

class WordPressIntegration:
    def __init__(self, config_manager):
        self.config = config_manager.get_credentials('wordpress')
        self.client = Client(
            self.config['url'],
            self.config['username'],
            self.config['password']
        )
        
    async def create_post(self, content: Dict) -> str:
        try:
            post = WordPressPost()
            post.title = content['title']
            post.content = self._prepare_content(content)
            post.terms_names = {
                'category': content['categories'],
                'post_tag': content['tags']
            }
            post.thumbnail = await self._upload_featured_image(content['featured_image'])
            
            return self.client.call(posts.NewPost(post))
        except Exception as e:
            logging.error(f"WordPress posting failed: {str(e)}")
            raise