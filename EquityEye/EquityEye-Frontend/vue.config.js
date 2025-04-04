const { defineConfig } = require('@vue/cli-service')
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // 没有 pathRewrite，所以 /api 不会被去掉
      }
    }
  }
}
