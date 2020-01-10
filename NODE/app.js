// const express = require('express')
// const fs = require('fs');
// const os = require('os');

// const app = express()
// const port = 8088

// const file = fs.readFileSync('./sample_product_data.tsv')
// //const data = file.toString().split()

// const model = () => {
//     var data = file.toString().split('/n')
//     data.forEach().map( (product) => {
//         var fields = product.trim().split('/t') // id desc 

//     })
// }

// app.post('/api/products/autocomplete', (req, res) => {
//     res.statusCode=200
//     res.append('Allow-Cross-Origin','allow')
//     res.send('Hello from Express')
// })
// app.listen(8088,(req,res)=>{
//     console.log('starting express server')
//     console.log('hello form server agian')
// })

//const data = file.split('\n').array.map((()=> {}))
// const http = require('http')
// const server = http.createServer((req, res) => {
//   res.statusCode = 200;
//   res.setHeader('Content-Type', 'text/plain');
//   res.end('Hello World\n');
// });

// server.listen('8088','localhost',() => {
//     console.log('Server Started at localhost:8088')
// })

const fs = require('fs');

function someAsyncOperation(callback) {
  // Assume this takes 95ms to complete
  fs.readFile('/sample_product_data.tsv', callback);
}

const timeoutScheduled = Date.now();

setTimeout(() => {
  const delay = Date.now() - timeoutScheduled;

  console.log(`${delay}ms have passed since I was scheduled`);
}, 10);


// do someAsyncOperation which takes 95 ms to complete
someAsyncOperation(() => {
  const startCallback = Date.now();

  // do something that will take 10ms...
  while (Date.now() - startCallback < 4) {
    // do nothing
    console.log(`${Date.now()} from last`)
  }
});

// Promise
var prom = new Promise(resolve,reject)
