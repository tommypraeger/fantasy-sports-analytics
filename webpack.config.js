import path from 'path';

module.exports = {
  entry: './app/static/js/index.js',
  output: {
    path: path.join(__dirname, 'app/static'),
    filename: 'bundle.js',
  },
  watch: true,
};