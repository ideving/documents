# tls && https

## 1. 简单介绍
1. 服务器 用RSA生成公钥和私钥

2. 把公钥放在证书里发送给客户端，私钥自己保存

3. 客户端首先向一个权威的服务器检查证书的合法性，如果证书合法，客户端产生一段随机数，这个随机数就作为通信的密钥，我们称之为对称密钥，用公钥加密这段随机数，然后发送到服务器

4. 服务器用私钥解密获取的对称密钥，然后，双方就已对称密钥进行加密解密通信了

PS:非对称的RSA加密性能是非常低的，原因在于寻找大素数、大数计算、数据分割需要耗费很多的CPU周期，所以一般的HTTPS连接只在第一次握手时使用非对称加密，通过握手交换对称加密密钥，在之后的通信走对称加密。

## 2. 详细介绍
1. 浏览器将自己支持的一套加密规则发送给网站。 

2. 网站从中选出一组加密算法与HASH算法，并将自己的身份信息以证书的形式发回给浏览器。证书里面包含了网站地址，加密公钥，以及证书的颁发机构等信息。 

3. 浏览器获得网站证书之后浏览器要做以下工作： 

    a) 验证证书的合法性（颁发证书的机构是否合法，证书中包含的网站地址是否与正在访问的地址一致等），如果证书受信任，则浏览器栏里面会显示一个小锁头，否则会给出证书不受信的提示。 
    
    b) 如果证书受信任，或者是用户接受了不受信的证书，浏览器会生成一串随机数的密码，并用证书中提供的公钥加密。 
    
    c) 使用约定好的HASH算法计算握手消息，并使用生成的随机数对消息进行加密，最后将之前生成的所有信息发送给网站。 
    
4. 网站接收浏览器发来的数据之后要做以下的操作： 

    a) 使用自己的私钥将信息解密取出密码，使用密码解密浏览器发来的握手消息，并验证HASH是否与浏览器发来的一致。 
    
    b) 使用密码加密一段握手消息，发送给浏览器。 
    
5. 浏览器解密并计算握手消息的HASH，如果与服务端发来的HASH一致，此时握手过程结束，之后所有的通信数据将由之前浏览器生成的随机密码并利用对称加密算法进行加密。

## 3. 实现

- 生成密钥、证书

> 第一步，为服务器端和客户端准备公钥、私钥
```batch
# 生成服务器端私钥
openssl genrsa -out server.key 1024
# 生成服务器端公钥
openssl rsa -in server.key -pubout -out server.pem

# 生成客户端私钥
openssl genrsa -out client.key 1024
# 生成客户端公钥
openssl rsa -in client.key -pubout -out client.pem
```

> 第二步，生成 CA 证书
```batch

# 生成 CA 私钥
openssl genrsa -out ca.key 1024
# X.509 Certificate Signing Request (CSR) Management.
openssl req -new -key ca.key -out ca.csr
# X.509 Certificate Data Management.
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt
```

> 在执行第二步时会出现
```batch
➜  keys  openssl req -new -key ca.key -out ca.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:Zhejiang
Locality Name (eg, city) []:Hangzhou
Organization Name (eg, company) [Internet Widgits Pty Ltd]:My CA
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:localhost
Email Address []:
```

注意，这里的 Organization Name (eg, company) [Internet Widgits Pty Ltd]: 后面生成客户端和服务器端证书的时候也需要填写，不要写成一样的！！！可以随意写如：My CA, My Server, My Client。

然后 Common Name (e.g. server FQDN or YOUR name) []: 这一项，是最后可以访问的域名，我这里为了方便测试，写成 localhost ，如果是为了给我的网站生成证书，需要写成 barretlee.com 。

> 第三步，生成服务器端证书和客户端证书
```batch
# 服务器端需要向 CA 机构申请签名证书，在申请签名证书之前依然是创建自己的 CSR 文件
openssl req -new -key server.key -out server.csr
# 向自己的 CA 机构申请证书，签名过程需要 CA 的证书和私钥参与，最终颁发一个带有 CA 签名的证书
openssl x509 -req -CA ca.crt -CAkey ca.key -CAcreateserial -in server.csr -out server.crt
 
# client 
openssl req -new -key client.key -out client.csr
# client 到 CA 签名
openssl x509 -req -CA ca.crt -CAkey ca.key -CAcreateserial -in client.csr -out client.crt
```

> 此时，我们的 keys 文件夹下已经有如下内容了
```batch
.
├── https-client.js
├── https-server.js
└── keys
    ├── ca.crt
    ├── ca.csr
    ├── ca.key
    ├── ca.pem
    ├── ca.srl
    ├── client.crt
    ├── client.csr
    ├── client.key
    ├── client.pem
    ├── server.crt
    ├── server.csr
    ├── server.key
    └── server.pem
```

> 看到上面两个 js 文件了么，我们来跑几个demo

## HTTPS本地测试

> 服务器代码
```batch
// file http-server.js
var https = require('https');
var fs = require('fs');
 
var options = {
  key: fs.readFileSync('./keys/server.key'),
  cert: fs.readFileSync('./keys/server.crt')
};
 
https.createServer(options, function(req, res) {
  res.writeHead(200);
  res.end('hello world');
}).listen(8000);
```

> 短短几行代码就构建了一个简单的 https 服务器，options 将私钥和证书带上。然后利用 curl 测试：
```batch
➜  https  curl https://localhost:8000
curl: (60) SSL certificate problem: Invalid certificate chain
More details here: http://curl.haxx.se/docs/sslcerts.html
 
curl performs SSL certificate verification by default, using a "bundle"
 of Certificate Authority (CA) public keys (CA certs). If the default
 bundle file isn't adequate, you can specify an alternate file
 using the --cacert option.
If this HTTPS server uses a certificate signed by a CA represented in
 the bundle, the certificate verification probably failed due to a
 problem with the certificate (it might be expired, or the name might
 not match the domain name in the URL).
If you'd like to turn off curl's verification of the certificate, use
 the -k (or --insecure) option.
```

> 当我们直接访问时， curl https://localhost:8000
  
> 一堆提示，原因是没有经过 CA 认证，添加 -k 参数能够解决这个问题：
```batch
➜  https  curl -k https://localhost:8000
hello world%
```

> 这样的方式是不安全的，存在我们上面提到的中间人攻击问题。可以搞一个客户端带上 CA 证书试试：
```batch
// file http-client.js
var https = require('https');
var fs = require('fs');
 
var options = {
  hostname: "localhost",
  port: 8000,
  path: '/',
  methed: 'GET',
  key: fs.readFileSync('./keys/client.key'),
  cert: fs.readFileSync('./keys/client.crt'),
  ca: [fs.readFileSync('./keys/ca.crt')]
};
 
options.agent = new https.Agent(options);
 
var req = https.request(options, function(res) {
  res.setEncoding('utf-8');
  res.on('data', function(d) {
    console.log(d);
  });
});
req.end();
 
req.on('error', function(e) {
  console.log(e);
});
```

> 先打开服务器 node http-server.js ，然后执行
```batch
➜  https  node https-client.js
hello world
```

> 如果你的代码没有输出 
  
> hello world ，说明证书生成的时候存在问题。也可以通过浏览器访问：

提示错误：

此服务器无法证明它是localhost；您计算机的操作系统不信任其安全证书。出现此问题的原因可能是配置有误或您的连接被拦截了。

原因是浏览器没有 CA 证书，只有 CA 证书，服务器才能够确定，这个用户就是真实的来自 localhost 的访问请求（比如不是代理过来的）。

你可以点击 继续前往localhost（不安全） 这个链接，相当于执行 curl -k https://localhost:8000 。如果我们的证书不是自己颁发，而是去靠谱的机构去申请的，那就不会出现这样的问题，因为靠谱机构的证书会放到浏览器中，浏览器会帮我们做很多事情。