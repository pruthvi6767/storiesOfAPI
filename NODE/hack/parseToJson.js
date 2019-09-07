const path = require('path')
const fs = require('fs')
const readline = require('readline')
const stream = require('stream')



const products = []
console.log(process.cwd())
//console.log(path.join(__dirname,'..','sample_product_data.tsv'))

// method 1 read via async method
// console.time()
// fs.readFile('./sample_product_data.tsv','utf-8',(err,data)=>{
//     if(err) throw err
//     console.log(data)
//     console.timeLog()
// })

// method2 read by create readstream and by each line 
var oStream = new stream()
var iStream = fs.createReadStream(path.join(__dirname,'..','sample_product_data.tsv'), {flags: 'r',encoding: 'utf8', autoClose: true})
console.time()
var line_data = readline.createInterface(iStream, oStream)
line_data.on('line', (line) => {
    let product = line.split('\t')
    products.push(productJSON(product))
    //console.log(product)
})
// iStream.on('end', () => {
//     console.log(products)
//     console.timeEnd()
//     line_data.close()
// })
line_data.on('close', () => {
    console.log(products)
    console.timeEnd()
    line_data.close()
})


function productJSON(items) {
    //console.log(items)
    let values = items.map( (value) => {
        data = String(value)
        if(!data) {
            data = ""
        }
        if(data.includes('"') ) {
            data.replace('"', '\"')
            console.log(data)
        }
        return data
    })
    //console.log(values)
    let product_json = JSON.parse(`{"productId": "${values[0]}","title": "${values[1]}",
        "brandId": "${values[2]}","brandName": "${values[3]}","categoryId": "${values[4]}",
        "categoryName": "${values[5]}"}`)
    return product_json
}








