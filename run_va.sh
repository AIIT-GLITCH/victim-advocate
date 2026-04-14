#!/bin/bash
cd /home/buddy_ai/apps/victim_advocate
exec python3 start_va.py >> /tmp/va.log 2>&1