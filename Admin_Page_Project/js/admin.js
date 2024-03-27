const cloth_type_button = document.getElementById('cloth_type');
const cloth_gender = document.getElementById('cloth_gender');
const dataTable = document.getElementById('data-table');
const searchButton = document.getElementById('search-button');
const inputText = document.getElementById('product_name_input');



// 사전정의 데이터(크롤링 코드 작성시 미사용)
const data = [
{ category: "상의", brand: 'Supreme', product: '슈프림 박스로고 후드티', price: '390,000',gender:'남성'},
{ category: "하의", brand: 'DIESEL', product: '디젤 트랙 팬츠', price: '188,000',gender:'여성' },
{ category: "신발", brand: 'Nike', product: '에어포스 1', price: '137,000' ,gender:'공용'},
{ category: "패션잡화", brand: 'Music&Goods', product: '빵빵이 키링', price: '29,000' ,gender:'공용'},
{ category: "상의", brand: 'Supreme', product: '슈프림 박스로고 후드티11', price: '390,000',gender:'남성'},
{ category: "하의", brand: 'DIESEL', product: '디젤 트랙 팬츠11', price: '188,000',gender:'여성' },
{ category: "신발", brand: 'Nike', product: '에어포스 1 11', price: '137,000' ,gender:'공용'},
{ category: "패션잡화", brand: 'Music&Goods', product: '빵빵이 키링11', price: '29,000' ,gender:'공용'},
{ category: "상의", brand: 'Supreme', product: '슈프림 박스로고 후드티22', price: '390,000',gender:'남성'},
{ category: "하의", brand: 'DIESEL', product: '디젤 트랙 팬츠22', price: '188,000',gender:'여성' },
{ category: "신발", brand: 'Nike', product: '에어포스 1 22', price: '137,000' ,gender:'공용'},
{ category: "패션잡화", brand: 'Music&Goods', product: '빵빵이 키링22', price: '29,000' ,gender:'공용'},    // ...
];

let filter_data = data

//테이블에 데이터 집어넣기
function insertTable(data){
    let product_num = 0;
    data.forEach((item) => {
        const row = dataTable.insertRow();
        row.insertCell(0).innerHTML = `<input class="form-check-input" type="checkbox" id="${product_num}_check">`
        row.insertCell(1).innerHTML = item.category;
        row.insertCell(2).innerHTML = item.brand;
        row.insertCell(3).innerHTML = item.product;
        row.insertCell(4).innerHTML = item.price;
        row.insertCell(5).innerHTML = item.gender;
        product_num += 1
    });
}
insertTable(data)

// 최종 업데이트 일자 반영
function set_Update_Date() {
    let time = new Date(document.lastModified);   
    const date_string = ('('+time.getFullYear()+'-'+(time.getMonth()+1)+'-'+time.getDate()+')');
    docTitle = document.getElementById('docTitle')
    docTitle.innerText += date_string
}

set_Update_Date()


function select_filter(){
    filter_data = data.filter(function(item){
        if (cloth_type_button.value == '전체'){
            return item.category
        }
        return item.category == cloth_type_button.value
        
    });
    filter_data = filter_data.filter(function(item){
        if (cloth_gender.value == '전체'){
            return item.gender
        }
        else if (item.gender == '공용'){
            return item.gender
        }
        return item.gender == cloth_gender.value
    });
    return filter_data
}

function search_filter(){
    filter_data = select_filter()
    console.log(filter_data)
    filter_data = filter_data.filter(function(item){
        if (item.product.includes(inputText.value) || item.brand.includes(inputText.value)) {
            return item.product
        }
    })
    return filter_data
}



// 이벤트 리스너
// 선택 옷종류
cloth_type_button.addEventListener('change', function(){
    dataTable.innerHTML = ''
    filter_data = select_filter()
    insertTable(filter_data)
});

//성별 선택
cloth_gender.addEventListener('change', function(){
    dataTable.innerHTML = ''
    filter_data = select_filter()
    insertTable(filter_data)
});

searchButton.addEventListener('click', function(e){
    e.preventDefault();
    dataTable.innerHTML = ''
    console.log('a')
    filter_data = search_filter()
    console.log(filter_data)
    insertTable(filter_data)
});
