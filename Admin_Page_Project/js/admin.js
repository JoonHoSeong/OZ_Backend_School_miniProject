
const data = [
{ category: "상의", brand: 'Supreme', product: '슈프림 박스로고 후드티', price: '390,000',gender:'남성'},
{ category: "하의", brand: 'DIESEL', product: '디젤 트랙 팬츠', price: '188,000',gender:'여성' },
{ category: "신발", brand: 'Nike', product: '에어포스 1', price: '137,000' ,gender:'공용'},
{ category: "패션잡화", brand: 'Music&Goods', product: '빵빵이 키링', price: '29,000' ,gender:'공용'},
    // ...
];

const dataTable = document.getElementById('data-table');
let product_num = 0;
data.forEach((item) => {
    console.log(item)
    const row = dataTable.insertRow();
    row.insertCell(0).innerHTML = `<input class="form-check-input" type="checkbox" id="${product_num}_check">`
    row.insertCell(1).innerHTML = item.category;
    row.insertCell(2).innerHTML = item.brand;
    row.insertCell(3).innerHTML = item.product;
    row.insertCell(4).innerHTML = item.price;
    row.insertCell(5).innerHTML = item.gender;
    product_num += 1
});


function set_Update_Date() {
    let time = new Date(document.lastModified);   
    const date_string = ('('+time.getFullYear()+'-'+(time.getMonth()+1)+'-'+time.getDate()+')');
    docTitle = document.getElementById('docTitle')
    docTitle.innerText += date_string
}

set_Update_Date()
