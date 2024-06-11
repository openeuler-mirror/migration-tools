// const {createProxyMiddleware} = require('http-proxy-middleware');
// module.exports = function (app) {
//     app.use('/httpServer', createProxyMiddleware({
//         target: 'http://10.12.21.202:9999',//后台服务器地址
//         changeOrigin: true,
//         pathRewrite: {
//             '^/httpServer': 'http://10.12.17.202:8080',//本地地址
//         },
//     }))
// }
