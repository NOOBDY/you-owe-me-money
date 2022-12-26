"""
# DB Module

This module acts as a middle layer that interacts with the database
"""
from .record import Record
from .utils import *
from supabase import create_client, Client