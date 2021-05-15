paypal.Buttons({
    createOrder: function () {
        alert('in create order')
        return fetch('create-paypal-transaction', {
            method: 'post',
            headers: {
                'content-type': 'application/json'
            }
        }).then(res => {
            // console.log("data here"+res.clone.json())
            
            return res.json()
    
            
        }).then( data=> {
            // console.log("id here"+data.clone.id)
            return data.id; // Use the key sent by your server's response, ex. 'id' or 'token'
        }).catch(error =>{
        console.log('error:')
        console.error(error);
        });
    },
    onApprove: function (data) {
        alert('in onaprove')
        return fetch('get-paypal-transaction', {
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify({
                orderID: data.orderID
            })
        }).then(function (res) {
            return res.json();
        }).then(function (details) {
            alert('Transaction approved by ' + details.payer_given_name);

        })
        }
}).render('#paypal-button');
