var updateBtn = document.getElementsByClassName('update-cart')
for (i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId , 'action:', action)


        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('User is not authenticated')
        }
        else{
            updateUserOrder(productId, action)
        }
    })

}
function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data...')

        var url = '/update_item/'

        fetch(url,{
            method:'POST',
            headers:{
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'productId':productId , 'action':action})
        })
        .then((response) => {
            return response.json();
        })
        .then((data) =>{
            console.log('data:', data)
            location.reload()
        });
}