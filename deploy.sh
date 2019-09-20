#!/bin/bash
aws s3 cp app/dist/ s3://fantasy-sports-analytics.com --recursive
eb deploy
