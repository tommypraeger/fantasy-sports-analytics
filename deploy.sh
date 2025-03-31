#!/bin/bash

if [[ $* != *--skip-react* ]]; then
    npm install
    npm run build
    aws s3 cp app/dist/ s3://fantasy-sports-analytics.com --recursive
    aws cloudfront create-invalidation --distribution-id EQ5A8DNTWQ42J --paths "/*"
fi
if [[ $* != *--skip-lambda* ]]; then
    # Use a temporary build directory to ensure clean packaging
    BUILD_DIR=lambda_build
    rm -rf $BUILD_DIR
    mkdir $BUILD_DIR
    mkdir -p $BUILD_DIR/site-packages

    # Install dependencies into the python subdirectory
    pip install \
      --platform manylinux2014_aarch64 \
      --target=$BUILD_DIR/site-packages \
      --implementation cp \
      --python-version 3.13 \
      --only-binary=:all: --upgrade \
      -r requirements.txt

    # Copy necessary source files while preserving structure
    cp application.py $BUILD_DIR
    mkdir -p $BUILD_DIR/app/analysis
    cp -r app/analysis $BUILD_DIR/app/
    cp app/__init__.py $BUILD_DIR/app/

    # Package into zip
    cd $BUILD_DIR
    zip -r ../app.zip .
    cd ..

    # Upload and update Lambda
    aws s3 cp app.zip s3://fantasy-sports-analytics
    aws lambda update-function-code --function-name fantasy-sports-analytics \
        --s3-bucket fantasy-sports-analytics \
        --s3-key app.zip

    # Clean up
    rm -rf $BUILD_DIR
    rm app.zip
fi
