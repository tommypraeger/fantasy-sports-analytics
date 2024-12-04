const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

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
