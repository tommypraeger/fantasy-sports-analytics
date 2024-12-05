const path = require('path');
const webpack = require('webpack');
const dotenv = require('dotenv');
const HtmlWebpackPlugin = require('html-webpack-plugin');

// Load environment variables
// Explicitly load .env
const env = dotenv.config({ path: './.env' }).parsed;

if (!env) {
  console.error('Failed to load .env file.');
} else {
  console.log('Loaded environment variables:', env);
}

module.exports = {
  entry: './app/static/js/index.jsx',
  output: {
    path: path.join(__dirname, 'app', 'dist'),
    filename: 'bundle.js',
    publicPath: '/',
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Fantasy Sports Analytics',
      template: './app/index.html',
      favicon: './app/favicon.ico',
    }),
    new webpack.DefinePlugin({
      'process.env': JSON.stringify(env),
    }),
  ],
  watch: false,
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        resolve: { extensions: ['.js', '.jsx'] },
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name]-[hash:8].[ext]',
            },
          },
        ],
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          // Creates `style` nodes from JS strings
          'style-loader',
          // Translates CSS into CommonJS
          'css-loader',
          // Compiles Sass to CSS
          'sass-loader',
        ],
      },
    ],
  },
  devServer: {
    static: {
      directory: path.join(__dirname, 'app', 'dist'),
    },
    compress: true,
    port: 8000,
    // proxy: {
    //   '/api': 'http://localhost:5000',
    // },
    historyApiFallback: true,
  },
};
