#!/bin/bash
# Deploy the front-end to S3/CloudFront and the back-end to Lambda.
# Run ./deploy.sh --help for options.

set -euo pipefail

# Print AWS CLI output directly instead of opening it in a pager
export AWS_PAGER=""

cd "$(dirname "$0")"

SITE_BUCKET=fantasy-sports-analytics.com
CLOUDFRONT_DISTRIBUTION_ID=EQ5A8DNTWQ42J
LAMBDA_BUCKET=fantasy-sports-analytics
LAMBDA_FUNCTION=fantasy-sports-analytics
# Must match the Lambda's runtime and architecture settings
LAMBDA_PYTHON_VERSION=3.13
LAMBDA_PLATFORM=manylinux2014_aarch64

BUILD_DIR=lambda_build
LAMBDA_ZIP=app.zip

if [[ -x venv/bin/python ]]; then
    PYTHON=venv/bin/python
else
    PYTHON=python3
fi

usage() {
    cat <<EOF
Usage: ./deploy.sh [options]

Options:
  --skip-react    Don't deploy the front-end
  --skip-lambda   Don't deploy the back-end
  --skip-tests    Don't run test_lambda.py before deploying the back-end
  --force         Don't ask for confirmation about uncommitted or unpushed changes
  -h, --help      Show this help
EOF
}

SKIP_REACT=false
SKIP_LAMBDA=false
SKIP_TESTS=false
FORCE=false
for arg in "$@"; do
    case $arg in
        --skip-react) SKIP_REACT=true ;;
        --skip-lambda) SKIP_LAMBDA=true ;;
        --skip-tests) SKIP_TESTS=true ;;
        --force) FORCE=true ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown option: $arg" >&2; usage >&2; exit 1 ;;
    esac
done

cleanup() {
    rm -rf "$BUILD_DIR" "$LAMBDA_ZIP"
}
trap cleanup EXIT

# Warn before deploying code that isn't on GitHub
if [[ $FORCE == false ]]; then
    warnings=()
    if [[ -n $(git status --porcelain) ]]; then
        warnings+=("You have uncommitted changes.")
    fi
    if git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
        unpushed=$(git rev-list --count '@{u}..HEAD')
        if [[ $unpushed -gt 0 ]]; then
            warnings+=("$(git branch --show-current) has $unpushed unpushed commit(s).")
        fi
    fi
    if [[ ${#warnings[@]} -gt 0 ]]; then
        printf '%s\n' "${warnings[@]}"
        read -r -p "Deploy anyway? [y/N] " answer
        [[ $answer == [yY] ]] || exit 1
    fi
fi

if [[ $SKIP_LAMBDA == false && $SKIP_TESTS == false ]]; then
    echo "Running tests..."
    "$PYTHON" -m unittest test_lambda.py
fi

if [[ $SKIP_REACT == false ]]; then
    echo "Deploying front-end..."
    npm ci
    npm run build
    aws s3 sync app/dist/ "s3://$SITE_BUCKET" --delete
    aws cloudfront create-invalidation \
        --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" \
        --paths "/*"
fi

if [[ $SKIP_LAMBDA == false ]]; then
    echo "Deploying back-end..."
    rm -rf "$BUILD_DIR" "$LAMBDA_ZIP"
    mkdir -p "$BUILD_DIR/site-packages"

    # Install Lambda dependencies for the Lambda's platform
    "$PYTHON" -m pip install \
        --platform "$LAMBDA_PLATFORM" \
        --target="$BUILD_DIR/site-packages" \
        --implementation cp \
        --python-version "$LAMBDA_PYTHON_VERSION" \
        --only-binary=:all: --upgrade --no-compile \
        -r requirements-lambda.txt

    # Copy necessary source files while preserving structure
    cp application.py "$BUILD_DIR"
    mkdir -p "$BUILD_DIR/app"
    cp app/__init__.py "$BUILD_DIR/app/"
    cp -r app/analysis "$BUILD_DIR/app/"
    find "$BUILD_DIR" -name __pycache__ -type d -prune -exec rm -rf {} +

    (cd "$BUILD_DIR" && zip -qr "../$LAMBDA_ZIP" .)

    # Upload and update Lambda
    aws s3 cp "$LAMBDA_ZIP" "s3://$LAMBDA_BUCKET/$LAMBDA_ZIP"
    aws lambda update-function-code \
        --function-name "$LAMBDA_FUNCTION" \
        --s3-bucket "$LAMBDA_BUCKET" \
        --s3-key "$LAMBDA_ZIP" \
        --query '{FunctionName: FunctionName, CodeSize: CodeSize, LastModified: LastModified}'
    echo "Waiting for Lambda update to finish..."
    aws lambda wait function-updated --function-name "$LAMBDA_FUNCTION"

    # Smoke test the deployed Lambda
    api_endpoint=$(grep '^API_ENDPOINT=' .env.production | cut -d= -f2-)
    response=$(curl -sS --fail --max-time 30 -X POST "$api_endpoint" \
        -H "Content-type: application/json; charset=UTF-8" \
        -d '{"method": "wakeup-league-analysis"}')
    if [[ $response != "{}" ]]; then
        echo "Smoke test failed: unexpected response from $api_endpoint: $response" >&2
        exit 1
    fi
    echo "Smoke test passed."
fi

echo "Deploy complete."
