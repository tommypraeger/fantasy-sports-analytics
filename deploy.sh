#!/bin/bash

if [[ $* != *--skip-react* ]]; then
    npm install
    npm run build
    aws s3 cp app/dist/ s3://fantasy-sports-analytics.com --recursive
    aws cloudfront create-invalidation --distribution-id EQ5A8DNTWQ42J --paths "/*"
fi
if [[ $* != *--skip-lambda* ]]; then
cd venv/lib/python3.8/site-packages
zip -r9 ${OLDPWD}/app.zip . -x "numpy*" "scipy*"
cd $OLDPWD
zip -rg app.zip . -x ".git*" "node_modules/*" "venv/*" "*.DS_Store"\
    ".vscode/*" "deploy.sh" "app/dist/*" "app/static/*" "*__pycache__/*"\
    "package.json" "package-lock.json" "webpack*" ".babelrc" ".env"\
    ".eslintrc.js" "README.md"
aws s3 cp app.zip s3://fantasy-sports-analytics
rm app.zip
aws lambda update-function-code --function-name fantasy-sports-analytics\
    --s3-bucket fantasy-sports-analytics\
    --s3-key app.zip
fi
