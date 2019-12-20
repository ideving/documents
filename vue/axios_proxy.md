### vue axios proxy
1. install axios
```cassandraql
npm install -S axios
```
2. main.js
```cassandraql
import axios from 'axios'
Vue.prototype.$http = axios
axios.defaults.baseURL = '/api'
```

3. vue.config.js
```cassandraql
module.exports = {
    configureWebpack: {
        devServer: {
            proxy: {
                '/*': {
                    target: 'http://localhost:8888/all',
                    changeOrigin: true,
                    secure: false,
                },
                '/api': {
                    target: 'http://localhost:9999/user',
                    changeOrigin: true,
                    secure: false,
                    pathRewrite: {
                        '^/api': ''
                    }
                }
            }
        }
    }
}
```

4. test
```cassandraql
//visit http://localhost:8888/all/test
this.$http.post("/test",{
    username:"admin",
    password:"123456"
})

//visit http://localhost:9999/user/login
this.$http.post("/login",{
    username:"admin",
    password:"123456"
})
```