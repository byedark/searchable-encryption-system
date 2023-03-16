module.exports = {
  assetsDir: 'static',
  outputDir: 'dist',
  indexPath:'index.html',
  //publicPath:"./",
  pages:{
    search:{
      entry:"./src/main.js",
      template:"./public/index.html",
      filename:"index.html",
      title:"可搜索机密云存储"
    },
  },
  //CORS跨域配置
  devServer: {
    host: '0.0.0.0', //可以忽略不写
    port: 8080, //它是用来修改你打开后的端口号的
    open: true, //值为 true的话，项目启动时自动打开到浏览器里边， false不会打开
    proxy: {
      '/api': {
        target: 'http://localhost:8000', //跨域请求的公共地址
        ws: false, //也可以忽略不写，不写不会影响跨域
        changeOrigin: true, //是否开启跨域，值为 true 就是开启， false 不开启
        pathRewrite: {
          '^/api': '' //注册全局路径， 但是在你请求的时候前面需要加上 /api
        }
      },
      '/file':{
        target: 'http://localhost:8000', //跨域请求的公共地址
        ws: false, //也可以忽略不写，不写不会影响跨域
        changeOrigin: true, //是否开启跨域，值为 true 就是开启， false 不开启
        pathRewrite: {
          '^/file': '' //注册全局路径， 但是在你请求的时候前面需要加上 /api
        }
      }
    }
  },
  runtimeCompiler:true
}
