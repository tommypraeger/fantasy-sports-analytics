const path = require('path');

module.exports = {
  entry: './app/static/js/index.js',
  output: {
    path: path.join(__dirname, 'app/static'),
    filename: 'bundle.js',
    publicPath: '/'
  },
  watch: true,
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          // Creates `style` nodes from JS strings
          'style-loader',
          // Translates CSS into CommonJS
          'css-loader',
          // Compiles Sass to CSS
          'sass-loader'
        ]
      }
    ]
  },
  devServer: {
    contentBase: path.join(__dirname, 'app'),
    compress: true,
    port: 8000,
    proxy: {
      '/api': 'http://localhost:5000'
    },
    historyApiFallback: true
  }
};
