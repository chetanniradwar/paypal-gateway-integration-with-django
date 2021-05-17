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
        window.open('failure-page')
        // console.log('error:')
        // console.error(error);
        // fetch('failure-page',{
        //     method:'get',

        // }).catch(error=>{
        //     console.error(error)
        // })
        });

    },
    onApprove: function (data) {
        alert('in onaprove')
        return fetch('capture-paypal-transaction', {
            method: 'post',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify({
                orderID: data.orderID
            })
        }).then( res=> {
            return res.json();
        }).then(function (details) { 
            // fetch('success-page',{
            //     method:'get',

            // }).catch(error=>{
            //     console.error(error)
            // })
            
            window.open('success-page');
            
//   alert('Transaction funds captured from' + details.payer_given_name);

        }).catch(error =>{
            // fetch('failure-page',{
            //     method:'get',

            // }).catch(error=>{
            //     console.error(error)
            // })
            window.open('failure-page')
            // console.log('error:')
            // console.error(error);
            });
        }
}).render('#paypal-button');
