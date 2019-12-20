### vue axios proxy
1. install axios
```cassandraql
npm install -S axios
```
2. main.js
```cassandraql
import axios from 'axios'
Vue.prototype.$http=axios
axios.defaults.baseURL = '/api'
```

3. vue.config.js
```cassandraql
module.exports = {
    configureWebpack: {
        devServer: {
            proxy: {
                '/api': {
                    target: 'http://localhost:8888/test',
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
//http://localhost:8888/test/user/login
this.$http.post("/user/login",{
    username:"admin",
    password:"123456"
})
```