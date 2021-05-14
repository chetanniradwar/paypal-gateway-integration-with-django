paypal.Buttons({
    createOrder: function () {
        return fetch('/create-paypal-transaction', {
            method: 'post',
            headers: {
                'content-type': 'application/json'
            }
        }).then(function (res) {
            return res.json();
        }).then(function (data) {
            return data.id; // Use the key sent by your server's response, ex. 'id' or 'token'
        })
    },
    onApprove: function (data) {
        return fetch('/get-paypal-transaction', {
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
