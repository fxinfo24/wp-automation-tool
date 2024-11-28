#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 03:01:42 2024

@author: thesaint
"""

# deploy.py
from src.deployment_manager import DeploymentManager
from src.version_control import VersionControl
import logging

def deploy():
    try:
        deployment = DeploymentManager()
        version_control = VersionControl()
        
        if deployment.validate_environment():
            config = deployment.load_config()
            version_control.increment_version('patch')
            version_control.log_change(
                'deployment',
                f'Deployed to {deployment.environment}'
            )
            logging.info(f"Deployed version {version_control.version}")
        else:
            raise ValueError("Invalid deployment configuration")
            
    except Exception as e:
        logging.error(f"Deployment failed: {str(e)}")
        raise

if __name__ == "__main__":
    deploy()